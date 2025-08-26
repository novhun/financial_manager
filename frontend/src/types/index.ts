// src/types/index.ts
export interface User {
  id: number;
  username: string;
  email: string;
  is_active: boolean;
}

export interface Token {
  access_token: string;
  token_type: string;
}

export interface Income {
  id: number;
  amount: number;
  type_id: number;
  description?: string;
  date?: string;
  group_id?: number;
  project_id?: number;
  user_id: number;
  type?: IncomeType;
}

export interface Expense {
  id: number;
  amount: number;
  type_id: number;
  description?: string;
  date?: string;
  group_id?: number;
  project_id?: number;
  user_id: number;
  type?: ExpenseType;
}

export interface Budget {
  id: number;
  category_id: number;
  amount: number;
  period: 'daily' | 'weekly' | 'monthly' | 'yearly';
  group_id?: number;
  project_id?: number;
  user_id: number;
  category?: BudgetCategory;
}

export interface Project {
  id: number;
  name: string;
  description?: string;
  start_date?: string;
  end_date?: string;
  image_url?: string;
  group_id?: number;
  user_id: number;
  tasks?: Task[];
}

export interface Task {
  id: number;
  name: string;
  status: 'pending' | 'in_progress' | 'done';
  start_date?: string;
  end_date?: string;
  file_url?: string;
  user_id?: number;
  project_id: number;
  assigned_user?: User;
}

export interface Group {
  id: number;
  name: string;
  description?: string;
  owner_id: number;
  members: User[];
}

export interface IncomeType {
  id: number;
  name: string;
  user_id?: number;
}

export interface ExpenseType {
  id: number;
  name: string;
  user_id?: number;
}

export interface BudgetCategory {
  id: number;
  name: string;
  user_id?: number;
}

export interface FinancialSummary {
  total_income: number;
  total_expense: number;
  net_balance: number;
  budget_status: Record<string, number>;
}

// Form types
export interface LoginForm {
  username: string;
  password: string;
}

export interface RegisterForm {
  username: string;
  email: string;
  password: string;
}

export interface ForgetPasswordForm {
  email: string;
}

export interface ResetPasswordForm {
  token: string;
  new_password: string;
}

export interface IncomeForm {
  amount: number;
  type_id: number;
  description?: string;
  date?: string;
  group_id?: number;
  project_id?: number;
}

export interface ExpenseForm {
  amount: number;
  type_id: number;
  description?: string;
  date?: string;
  group_id?: number;
  project_id?: number;
}

export interface BudgetForm {
  category_id: number;
  amount: number;
  period: 'daily' | 'weekly' | 'monthly' | 'yearly';
  group_id?: number;
  project_id?: number;
}

export interface ProjectForm {
  name: string;
  description?: string;
  start_date?: string;
  end_date?: string;
  image_url?: string;
  group_id?: number;
}

export interface TaskForm {
  name: string;
  status: 'pending' | 'in_progress' | 'done';
  start_date?: string;
  end_date?: string;
  file_url?: string;
  user_id?: number;
}