import axios from 'axios'

export const api = axios.create({ baseURL: import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000' })
api.interceptors.request.use(config => {
  const token = localStorage.getItem('finsight_token')
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

export type User = { id: string; name: string; email: string }
export type Category = { id: string; name: string; type: 'income' | 'expense' }
export type Transaction = { id: string; amount: number; type: 'income' | 'expense'; description: string; transaction_date: string; category_id: string | null; category?: Category | null }
export type Overview = { month: number; year: number; income: number; expenses: number; net_cash_flow: number; savings_rate: number | null; categories: { name: string; amount: number }[]; trend: { month: string; income: number; expenses: number }[] }
