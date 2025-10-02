-- ========================================
-- CONFIGURAÇÕES SUPABASE - DEMOCRATIZA AI
-- Execute estes comandos no Supabase SQL Editor
-- ========================================

-- 1. HABILITAR ROW LEVEL SECURITY (RLS)
-- ========================================

-- Habilitar RLS em todas as tabelas principais
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE contracts ENABLE ROW LEVEL SECURITY;
ALTER TABLE contract_analyses ENABLE ROW LEVEL SECURITY;
ALTER TABLE chat_sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE chat_messages ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_configurations ENABLE ROW LEVEL SECURITY;
ALTER TABLE document_vectors ENABLE ROW LEVEL SECURITY;
ALTER TABLE audit_logs ENABLE ROW LEVEL SECURITY;

-- 2. POLÍTICAS DE SEGURANÇA
-- ========================================

-- Usuários podem ver apenas seus próprios dados
CREATE POLICY "Users can view own profile" ON users
    FOR SELECT USING (auth.uid() = supabase_user_id);

CREATE POLICY "Users can update own profile" ON users
    FOR UPDATE USING (auth.uid() = supabase_user_id);

-- Contratos: usuários veem apenas os próprios
CREATE POLICY "Users can view own contracts" ON contracts
    FOR ALL USING (
        user_id IN (
            SELECT id FROM users WHERE supabase_user_id = auth.uid()
        )
    );

-- Análises: usuários veem apenas as próprias
CREATE POLICY "Users can view own analyses" ON contract_analyses
    FOR ALL USING (
        user_id IN (
            SELECT id FROM users WHERE supabase_user_id = auth.uid()
        )
    );

-- Chat: usuários acessam apenas seus próprios chats
CREATE POLICY "Users can access own chat sessions" ON chat_sessions
    FOR ALL USING (
        user_id IN (
            SELECT id FROM users WHERE supabase_user_id = auth.uid()
        )
    );

-- Mensagens: através das sessões do usuário
CREATE POLICY "Users can access own messages" ON chat_messages
    FOR ALL USING (
        session_id IN (
            SELECT cs.id FROM chat_sessions cs
            JOIN users u ON cs.user_id = u.id
            WHERE u.supabase_user_id = auth.uid()
        )
    );

-- Configurações: apenas as próprias
CREATE POLICY "Users can manage own config" ON user_configurations
    FOR ALL USING (
        user_id IN (
            SELECT id FROM users WHERE supabase_user_id = auth.uid()
        )
    );

-- Vetores de documentos: através dos contratos
CREATE POLICY "Users can access own document vectors" ON document_vectors
    FOR ALL USING (
        contract_id IN (
            SELECT c.id FROM contracts c
            JOIN users u ON c.user_id = u.id
            WHERE u.supabase_user_id = auth.uid()
        )
    );

-- Logs de auditoria: apenas os próprios
CREATE POLICY "Users can view own audit logs" ON audit_logs
    FOR SELECT USING (
        user_id IN (
            SELECT id FROM users WHERE supabase_user_id = auth.uid()
        )
    );

-- 3. CONFIGURAR COLUNA DE EMBEDDING PARA RAG
-- ========================================

-- Adicionar coluna de embedding (1536 dimensões para OpenAI/Claude embeddings)
ALTER TABLE document_vectors ADD COLUMN embedding vector(1536);

-- Criar índice para busca eficiente de vetores
CREATE INDEX ON document_vectors USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);

-- 4. TRIGGERS PARA TIMESTAMPS AUTOMÁTICOS
-- ========================================

-- Função para atualizar updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = now();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Aplicar trigger em tabelas com updated_at
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_contracts_updated_at BEFORE UPDATE ON contracts
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_analyses_updated_at BEFORE UPDATE ON contract_analyses
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_chat_sessions_updated_at BEFORE UPDATE ON chat_sessions
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_user_config_updated_at BEFORE UPDATE ON user_configurations
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- 5. FUNÇÃO PARA BUSCA SEMÂNTICA (RAG)
-- ========================================

CREATE OR REPLACE FUNCTION search_documents(
    query_embedding vector(1536),
    match_threshold float,
    match_count int,
    user_contract_ids uuid[]
)
RETURNS TABLE (
    id uuid,
    contract_id uuid,
    text_chunk text,
    chunk_index int,
    similarity float
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT
        dv.id,
        dv.contract_id,
        dv.text_chunk,
        dv.chunk_index,
        (1 - (dv.embedding <=> query_embedding)) AS similarity
    FROM document_vectors dv
    WHERE 
        dv.contract_id = ANY(user_contract_ids)
        AND (1 - (dv.embedding <=> query_embedding)) > match_threshold
    ORDER BY dv.embedding <=> query_embedding
    LIMIT match_count;
END;
$$;

-- 6. CONFIGURAÇÕES DE STORAGE (BUCKETS)
-- ========================================

-- Criar bucket para documentos (execute no painel Storage)
-- INSERT INTO storage.buckets (id, name, public, file_size_limit, allowed_mime_types)
-- VALUES (
--     'contracts',
--     'contracts', 
--     false,
--     26214400, -- 25MB
--     ARRAY['application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'text/plain']
-- );

-- Políticas para Storage
-- CREATE POLICY "Users can upload own contracts" ON storage.objects
--     FOR INSERT WITH CHECK (
--         bucket_id = 'contracts' 
--         AND auth.uid()::text = (storage.foldername(name))[1]
--     );

-- CREATE POLICY "Users can view own contracts" ON storage.objects
--     FOR SELECT USING (
--         bucket_id = 'contracts'
--         AND auth.uid()::text = (storage.foldername(name))[1]
--     );

-- 7. FUNÇÕES AUXILIARES
-- ========================================

-- Função para criar usuário quando se registra via Auth
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS trigger
LANGUAGE plpgsql
SECURITY DEFINER SET search_path = public
AS $$
BEGIN
    INSERT INTO public.users (
        supabase_user_id,
        email,
        full_name,
        avatar_url,
        subscription_plan,
        credits_remaining
    )
    VALUES (
        NEW.id,
        NEW.email,
        COALESCE(NEW.raw_user_meta_data->>'full_name', NEW.email),
        NEW.raw_user_meta_data->>'avatar_url',
        'free',
        3
    );
    RETURN NEW;
END;
$$;

-- Trigger para criar usuário automaticamente
DROP TRIGGER IF EXISTS on_auth_user_created ON auth.users;
CREATE TRIGGER on_auth_user_created
    AFTER INSERT ON auth.users
    FOR EACH ROW EXECUTE FUNCTION public.handle_new_user();

-- 8. ÍNDICES PARA PERFORMANCE
-- ========================================

-- Índices para consultas frequentes
CREATE INDEX IF NOT EXISTS idx_contracts_user_created ON contracts(user_id, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_analyses_contract_status ON contract_analyses(contract_id, status);
CREATE INDEX IF NOT EXISTS idx_chat_messages_session_created ON chat_messages(session_id, created_at ASC);
CREATE INDEX IF NOT EXISTS idx_audit_logs_user_action ON audit_logs(user_id, action, created_at DESC);

-- ========================================
-- CONFIGURAÇÃO COMPLETA!
-- 
-- Após executar todos esses comandos:
-- 1. Suas tabelas terão segurança RLS
-- 2. Usuários só verão próprios dados  
-- 3. pg_vector estará configurado para RAG
-- 4. Timestamps automáticos funcionando
-- 5. Integração com Supabase Auth
-- ========================================