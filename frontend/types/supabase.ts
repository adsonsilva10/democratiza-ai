// types/supabase.ts
export type Json =
  | string
  | number
  | boolean
  | null
  | { [key: string]: Json | undefined }
  | Json[]

export interface Database {
  public: {
    Tables: {
      users: {
        Row: {
          id: string
          email: string
          full_name: string | null
          created_at: string | null
          updated_at: string | null
          subscription_plan: string | null
          subscription_status: string | null
          subscription_expires_at: string | null
          credits_remaining: number | null
        }
        Insert: {
          id?: string
          email: string
          full_name?: string | null
          created_at?: string | null
          updated_at?: string | null
          subscription_plan?: string | null
          subscription_status?: string | null
          subscription_expires_at?: string | null
          credits_remaining?: number | null
        }
        Update: {
          id?: string
          email?: string
          full_name?: string | null
          created_at?: string | null
          updated_at?: string | null
          subscription_plan?: string | null
          subscription_status?: string | null
          subscription_expires_at?: string | null
          credits_remaining?: number | null
        }
      }
      contracts: {
        Row: {
          id: string
          user_id: string
          filename: string
          file_size: number | null
          mime_type: string | null
          storage_key: string | null
          contract_type: string | null
          processing_status: string | null
          risk_level: string | null
          risk_score: number | null
          created_at: string | null
          updated_at: string | null
        }
        Insert: {
          id?: string
          user_id: string
          filename: string
          file_size?: number | null
          mime_type?: string | null
          storage_key?: string | null
          contract_type?: string | null
          processing_status?: string | null
          risk_level?: string | null
          risk_score?: number | null
          created_at?: string | null
          updated_at?: string | null
        }
        Update: {
          id?: string
          user_id?: string
          filename?: string
          file_size?: number | null
          mime_type?: string | null
          storage_key?: string | null
          contract_type?: string | null
          processing_status?: string | null
          risk_level?: string | null
          risk_score?: number | null
          created_at?: string | null
          updated_at?: string | null
        }
      }
    }
    Views: {
      [_ in never]: never
    }
    Functions: {
      [_ in never]: never
    }
    Enums: {
      [_ in never]: never
    }
  }
}

// Helper types
export type User = Database['public']['Tables']['users']['Row']
export type Contract = Database['public']['Tables']['contracts']['Row']
export type UserInsert = Database['public']['Tables']['users']['Insert']
export type ContractInsert = Database['public']['Tables']['contracts']['Insert']