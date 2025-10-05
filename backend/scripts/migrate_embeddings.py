"""
Embedding Migration Script
Migra embeddings entre diferentes providers (Gemini ↔ OpenAI ↔ Anthropic)
"""
import asyncio
import argparse
import sys
from typing import List, Optional
from datetime import datetime
import logging

from sqlalchemy import select, func, update
from sqlalchemy.ext.asyncio import AsyncSession

# Add backend to path
sys.path.insert(0, '../')

from app.db.session import get_session
from app.models.legal_knowledge import LegalChunk, LegalDocument
from app.services.rag_service import RAGService, EmbeddingProvider
from app.core.config import settings

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class EmbeddingMigrator:
    """Handles migration of embeddings between providers"""
    
    def __init__(
        self,
        from_provider: EmbeddingProvider,
        to_provider: EmbeddingProvider,
        batch_size: int = 50,
        dry_run: bool = False
    ):
        self.from_provider = from_provider
        self.to_provider = to_provider
        self.batch_size = batch_size
        self.dry_run = dry_run
        
        # Initialize RAG services
        self.source_rag = RAGService(provider=from_provider)
        self.target_rag = RAGService(provider=to_provider)
        
        # Stats
        self.stats = {
            'total_chunks': 0,
            'migrated': 0,
            'failed': 0,
            'skipped': 0,
            'start_time': None,
            'end_time': None
        }
    
    async def get_total_chunks(self, db: AsyncSession) -> int:
        """Get total number of chunks to migrate"""
        result = await db.execute(
            select(func.count(LegalChunk.id))
        )
        return result.scalar()
    
    async def get_chunks_batch(
        self, 
        db: AsyncSession, 
        offset: int, 
        limit: int
    ) -> List[LegalChunk]:
        """Get a batch of chunks to migrate"""
        result = await db.execute(
            select(LegalChunk)
            .offset(offset)
            .limit(limit)
            .order_by(LegalChunk.id)
        )
        return result.scalars().all()
    
    async def migrate_chunk(
        self, 
        chunk: LegalChunk, 
        db: AsyncSession
    ) -> bool:
        """Migrate a single chunk"""
        try:
            # Skip if content is empty
            if not chunk.content or not chunk.content.strip():
                logger.warning(f"Chunk {chunk.id} has empty content, skipping")
                self.stats['skipped'] += 1
                return False
            
            # Create new embedding with target provider
            logger.debug(f"Creating embedding for chunk {chunk.id} ({len(chunk.content)} chars)")
            new_embedding = await self.target_rag.create_embeddings([chunk.content])
            
            if not new_embedding or len(new_embedding) == 0:
                logger.error(f"Failed to create embedding for chunk {chunk.id}")
                self.stats['failed'] += 1
                return False
            
            # Validate dimensions
            expected_dim = self.target_rag.embedding_dimension
            actual_dim = len(new_embedding[0])
            
            if actual_dim != expected_dim:
                logger.error(
                    f"Dimension mismatch for chunk {chunk.id}: "
                    f"expected {expected_dim}, got {actual_dim}"
                )
                self.stats['failed'] += 1
                return False
            
            if not self.dry_run:
                # Update chunk with new embedding
                chunk.embedding = new_embedding[0]
                chunk.updated_at = datetime.utcnow()
                
                # Add metadata about migration
                if not chunk.metadata:
                    chunk.metadata = {}
                
                chunk.metadata['embedding_provider'] = self.to_provider.value
                chunk.metadata['embedding_dimension'] = expected_dim
                chunk.metadata['migrated_from'] = self.from_provider.value
                chunk.metadata['migration_date'] = datetime.utcnow().isoformat()
                
                db.add(chunk)
            
            self.stats['migrated'] += 1
            return True
            
        except Exception as e:
            logger.error(f"Error migrating chunk {chunk.id}: {e}")
            self.stats['failed'] += 1
            return False
    
    async def migrate_all(self, db: AsyncSession):
        """Migrate all chunks"""
        logger.info(f"\n{'='*80}")
        logger.info(f"🔄 Starting Embedding Migration")
        logger.info(f"{'='*80}\n")
        logger.info(f"Source Provider: {self.from_provider.value} ({self.source_rag.embedding_dimension}d)")
        logger.info(f"Target Provider: {self.to_provider.value} ({self.target_rag.embedding_dimension}d)")
        logger.info(f"Batch Size: {self.batch_size}")
        logger.info(f"Mode: {'DRY RUN (no changes)' if self.dry_run else 'LIVE (will update database)'}")
        
        # Get total
        total = await self.get_total_chunks(db)
        self.stats['total_chunks'] = total
        
        if total == 0:
            logger.warning("No chunks found to migrate!")
            return
        
        logger.info(f"\n📊 Total chunks to migrate: {total}\n")
        
        if not self.dry_run:
            confirm = input("⚠️  This will modify the database. Continue? (yes/no): ")
            if confirm.lower() != 'yes':
                logger.info("Migration cancelled by user")
                return
        
        self.stats['start_time'] = datetime.utcnow()
        
        # Process in batches
        offset = 0
        batch_num = 1
        total_batches = (total + self.batch_size - 1) // self.batch_size
        
        while offset < total:
            logger.info(f"\n📦 Processing batch {batch_num}/{total_batches} (offset {offset})...")
            
            # Get batch
            chunks = await self.get_chunks_batch(db, offset, self.batch_size)
            
            if not chunks:
                break
            
            # Process each chunk in batch
            for i, chunk in enumerate(chunks, 1):
                success = await self.migrate_chunk(chunk, db)
                
                if success:
                    logger.info(
                        f"  ✅ [{batch_num}.{i}] Chunk {chunk.id}: "
                        f"{len(chunk.content)} chars → {self.target_rag.embedding_dimension}d"
                    )
                elif self.stats['skipped'] > self.stats['failed']:
                    logger.debug(f"  ⏭️  [{batch_num}.{i}] Chunk {chunk.id}: Skipped")
                else:
                    logger.error(f"  ❌ [{batch_num}.{i}] Chunk {chunk.id}: Failed")
            
            # Commit batch if not dry run
            if not self.dry_run:
                await db.commit()
                logger.info(f"  💾 Batch {batch_num} committed to database")
            
            # Progress
            progress = min(offset + self.batch_size, total)
            percentage = (progress / total) * 100
            logger.info(f"  📊 Progress: {progress}/{total} ({percentage:.1f}%)")
            
            offset += self.batch_size
            batch_num += 1
            
            # Rate limiting for Gemini
            if self.to_provider == EmbeddingProvider.GEMINI:
                logger.debug("  ⏱️  Sleeping 5s for Gemini rate limits...")
                await asyncio.sleep(5)
        
        self.stats['end_time'] = datetime.utcnow()
        self.print_stats()
    
    def print_stats(self):
        """Print migration statistics"""
        duration = (self.stats['end_time'] - self.stats['start_time']).total_seconds()
        
        logger.info(f"\n{'='*80}")
        logger.info(f"📊 Migration Complete!")
        logger.info(f"{'='*80}\n")
        logger.info(f"Total Chunks: {self.stats['total_chunks']}")
        logger.info(f"✅ Migrated: {self.stats['migrated']}")
        logger.info(f"❌ Failed: {self.stats['failed']}")
        logger.info(f"⏭️  Skipped: {self.stats['skipped']}")
        logger.info(f"⏱️  Duration: {duration:.1f}s")
        
        if self.stats['migrated'] > 0:
            rate = self.stats['migrated'] / duration
            logger.info(f"⚡ Rate: {rate:.2f} chunks/second")
        
        if self.dry_run:
            logger.info(f"\n⚠️  DRY RUN: No changes were made to the database")
        else:
            logger.info(f"\n✅ Database updated successfully")
        
        success_rate = (self.stats['migrated'] / self.stats['total_chunks'] * 100) if self.stats['total_chunks'] > 0 else 0
        logger.info(f"📈 Success Rate: {success_rate:.1f}%\n")


async def validate_migration(db: AsyncSession, target_provider: EmbeddingProvider):
    """Validate that migration was successful"""
    logger.info(f"\n{'='*80}")
    logger.info(f"🔍 Validating Migration")
    logger.info(f"{'='*80}\n")
    
    # Get sample chunks
    result = await db.execute(
        select(LegalChunk)
        .limit(10)
        .order_by(func.random())
    )
    chunks = result.scalars().all()
    
    target_rag = RAGService(provider=target_provider)
    expected_dim = target_rag.embedding_dimension
    
    all_valid = True
    
    for chunk in chunks:
        if not chunk.embedding:
            logger.error(f"❌ Chunk {chunk.id} has no embedding!")
            all_valid = False
            continue
        
        actual_dim = len(chunk.embedding)
        
        if actual_dim != expected_dim:
            logger.error(
                f"❌ Chunk {chunk.id}: dimension mismatch "
                f"(expected {expected_dim}, got {actual_dim})"
            )
            all_valid = False
        else:
            logger.info(f"✅ Chunk {chunk.id}: {actual_dim}d embedding OK")
        
        # Check metadata
        if chunk.metadata and 'embedding_provider' in chunk.metadata:
            provider = chunk.metadata['embedding_provider']
            if provider == target_provider.value:
                logger.info(f"   Provider metadata: {provider} ✅")
            else:
                logger.warning(f"   Provider metadata mismatch: {provider} ≠ {target_provider.value}")
    
    if all_valid:
        logger.info(f"\n✅ Validation passed! All embeddings have correct dimensions.")
    else:
        logger.error(f"\n❌ Validation failed! Some embeddings have issues.")
    
    return all_valid


async def main():
    """Main migration script"""
    parser = argparse.ArgumentParser(
        description='Migrate embeddings between providers',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  # Dry run (no changes)
  python migrate_embeddings.py --from gemini --to openai --dry-run
  
  # Migrate from Gemini to OpenAI
  python migrate_embeddings.py --from gemini --to openai --batch-size 100
  
  # Migrate from OpenAI to Gemini (for cost savings)
  python migrate_embeddings.py --from openai --to gemini --batch-size 10
  
  # Validate after migration
  python migrate_embeddings.py --validate openai
        '''
    )
    
    parser.add_argument(
        '--from',
        dest='from_provider',
        choices=['gemini', 'openai', 'anthropic'],
        help='Source provider'
    )
    
    parser.add_argument(
        '--to',
        dest='to_provider',
        choices=['gemini', 'openai', 'anthropic'],
        help='Target provider'
    )
    
    parser.add_argument(
        '--batch-size',
        type=int,
        default=50,
        help='Number of chunks to process per batch (default: 50)'
    )
    
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Simulate migration without making changes'
    )
    
    parser.add_argument(
        '--validate',
        choices=['gemini', 'openai', 'anthropic'],
        help='Validate existing embeddings for a provider'
    )
    
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose logging'
    )
    
    args = parser.parse_args()
    
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    
    # Validation mode
    if args.validate:
        provider_map = {
            'gemini': EmbeddingProvider.GEMINI,
            'openai': EmbeddingProvider.OPENAI,
            'anthropic': EmbeddingProvider.ANTHROPIC
        }
        
        async with get_session() as db:
            success = await validate_migration(db, provider_map[args.validate])
            sys.exit(0 if success else 1)
        return
    
    # Migration mode
    if not args.from_provider or not args.to_provider:
        parser.error("Both --from and --to are required for migration")
    
    if args.from_provider == args.to_provider:
        parser.error("Source and target providers must be different")
    
    # Map string to enum
    provider_map = {
        'gemini': EmbeddingProvider.GEMINI,
        'openai': EmbeddingProvider.OPENAI,
        'anthropic': EmbeddingProvider.ANTHROPIC
    }
    
    from_provider = provider_map[args.from_provider]
    to_provider = provider_map[args.to_provider]
    
    # Create migrator
    migrator = EmbeddingMigrator(
        from_provider=from_provider,
        to_provider=to_provider,
        batch_size=args.batch_size,
        dry_run=args.dry_run
    )
    
    # Run migration
    async with get_session() as db:
        try:
            await migrator.migrate_all(db)
        except KeyboardInterrupt:
            logger.warning("\n\n⚠️  Migration interrupted by user")
            migrator.print_stats()
            sys.exit(1)
        except Exception as e:
            logger.error(f"\n\n❌ Migration failed: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
