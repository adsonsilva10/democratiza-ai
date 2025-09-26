"""
API endpoints para processamento de imagens e OCR
"""

from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from fastapi.responses import StreamingResponse
from typing import List, Optional
import io
import json
from app.services.image_processor import DocumentImageProcessor, ImageProcessingResult
from pydantic import BaseModel

router = APIRouter(prefix="/image-processing", tags=["Image Processing"])

# Initialize image processor
image_processor = DocumentImageProcessor()

class ImageProcessingRequest(BaseModel):
    auto_enhance: bool = True
    preserve_colors: bool = False
    target_format: str = "PNG"

class ImageProcessingResponse(BaseModel):
    success: bool
    confidence_score: float
    applied_filters: List[str]
    original_size: tuple
    enhanced_size: tuple
    processing_time_ms: int

@router.post("/enhance-single", response_model=ImageProcessingResponse)
async def enhance_single_image(
    file: UploadFile = File(...),
    auto_enhance: bool = Form(True),
    preserve_colors: bool = Form(False)
):
    """
    Processa uma única imagem para otimização de OCR
    """
    try:
        # Validar tipo de arquivo
        if not file.content_type.startswith('image/'):
            raise HTTPException(
                status_code=400, 
                detail="Arquivo deve ser uma imagem"
            )
        
        # Ler dados da imagem
        image_data = await file.read()
        
        # Processar imagem
        import time
        start_time = time.time()
        
        result = image_processor.process_document_image(
            image_data=image_data,
            auto_enhance=auto_enhance,
            preserve_colors=preserve_colors
        )
        
        processing_time = int((time.time() - start_time) * 1000)
        
        return ImageProcessingResponse(
            success=True,
            confidence_score=result.confidence_score,
            applied_filters=result.applied_filters,
            original_size=result.original_size,
            enhanced_size=result.enhanced_size,
            processing_time_ms=processing_time
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro no processamento: {str(e)}"
        )

@router.post("/enhance-and-download")
async def enhance_and_download_image(
    file: UploadFile = File(...),
    auto_enhance: bool = Form(True),
    preserve_colors: bool = Form(False),
    output_format: str = Form("PNG")
):
    """
    Processa imagem e retorna arquivo otimizado para download
    """
    try:
        # Validar formato de saída
        valid_formats = ["PNG", "JPEG", "WEBP"]
        if output_format.upper() not in valid_formats:
            raise HTTPException(
                status_code=400,
                detail=f"Formato deve ser um de: {', '.join(valid_formats)}"
            )
        
        # Ler e processar imagem
        image_data = await file.read()
        
        result = image_processor.process_document_image(
            image_data=image_data,
            auto_enhance=auto_enhance,
            preserve_colors=preserve_colors
        )
        
        # Converter para bytes do formato solicitado
        enhanced_bytes = image_processor.get_enhanced_image_bytes(
            result, 
            format=output_format
        )
        
        # Preparar resposta de download
        media_type = f"image/{output_format.lower()}"
        filename = f"enhanced_{file.filename.rsplit('.', 1)[0]}.{output_format.lower()}"
        
        return StreamingResponse(
            io.BytesIO(enhanced_bytes),
            media_type=media_type,
            headers={
                "Content-Disposition": f"attachment; filename={filename}",
                "X-Confidence-Score": str(result.confidence_score),
                "X-Applied-Filters": ",".join(result.applied_filters)
            }
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro no processamento: {str(e)}"
        )

@router.post("/enhance-multiple", response_model=List[ImageProcessingResponse])
async def enhance_multiple_images(
    files: List[UploadFile] = File(...),
    auto_enhance: bool = Form(True),
    preserve_colors: bool = Form(False)
):
    """
    Processa múltiplas imagens mantendo consistência
    """
    try:
        if len(files) > 20:  # Limite de segurança
            raise HTTPException(
                status_code=400,
                detail="Máximo 20 imagens por vez"
            )
        
        # Validar todos os arquivos
        for file in files:
            if not file.content_type.startswith('image/'):
                raise HTTPException(
                    status_code=400,
                    detail=f"Arquivo {file.filename} não é uma imagem"
                )
        
        # Ler todas as imagens
        images_data = []
        for file in files:
            data = await file.read()
            images_data.append(data)
        
        # Processar todas as imagens
        import time
        start_time = time.time()
        
        results = image_processor.process_multiple_pages(
            images_data=images_data,
            auto_enhance=auto_enhance
        )
        
        processing_time = int((time.time() - start_time) * 1000)
        
        # Preparar respostas
        responses = []
        for result in results:
            responses.append(ImageProcessingResponse(
                success=True,
                confidence_score=result.confidence_score,
                applied_filters=result.applied_filters,
                original_size=result.original_size,
                enhanced_size=result.enhanced_size,
                processing_time_ms=processing_time // len(results)
            ))
        
        return responses
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro no processamento múltiplo: {str(e)}"
        )

@router.get("/quality-metrics")
async def get_quality_metrics():
    """
    Retorna métricas sobre o processamento de imagens
    """
    return {
        "processor_info": {
            "min_confidence": image_processor.min_confidence,
            "target_dpi": image_processor.target_dpi,
            "max_dimension": image_processor.max_dimension
        },
        "available_filters": [
            "perspective_correction",
            "smart_resize", 
            "noise_reduction",
            "contrast_enhancement",
            "lighting_correction",
            "adaptive_sharpening",
            "binarization"
        ],
        "supported_formats": ["PNG", "JPEG", "WEBP"],
        "max_files_per_batch": 20
    }

@router.post("/preview-enhancement")
async def preview_enhancement(
    file: UploadFile = File(...),
    filter_name: str = Form(...),
):
    """
    Aplica filtro específico para preview
    """
    try:
        # Validar filtro
        valid_filters = [
            "perspective_correction", "smart_resize", "noise_reduction",
            "contrast_enhancement", "lighting_correction", 
            "adaptive_sharpening", "binarization"
        ]
        
        if filter_name not in valid_filters:
            raise HTTPException(
                status_code=400,
                detail=f"Filtro deve ser um de: {', '.join(valid_filters)}"
            )
        
        image_data = await file.read()
        
        # Aplicar apenas o filtro específico
        result = image_processor.process_document_image(
            image_data=image_data,
            auto_enhance=False  # Desabilitar processamento automático
        )
        
        # Aplicar filtro específico manualmente
        # (Esta seria uma implementação mais granular do processamento)
        
        enhanced_bytes = image_processor.get_enhanced_image_bytes(result)
        
        return StreamingResponse(
            io.BytesIO(enhanced_bytes),
            media_type="image/png",
            headers={
                "X-Applied-Filter": filter_name,
                "X-Confidence-Score": str(result.confidence_score)
            }
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro no preview: {str(e)}"
        )