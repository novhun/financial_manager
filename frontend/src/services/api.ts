// src/services/api.ts
import axios from 'axios';
import { 
  LoginForm, 
  RegisterForm, 
  ForgetPasswordForm, 
  ResetPasswordForm,
  IncomeForm,
  ExpenseForm,
  BudgetForm,
  ProjectForm,
  TaskForm,
  IncomeType,
  ExpenseType,
  BudgetCategory,
  User,
  Income,
  Expense,
  Budget,
  Project,
  Task,
  Group,
  FinancialSummary
} from '../types';

const API_BASE_URL = 'http://127.0.0.1:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
});

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle auth errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export const authAPI = {
  login: async (data: LoginForm) => {
    const formData = new URLSearchParams();
    formData.append('username', data.username);
    formData.append('password', data.password);
    
    const response = await api.post('/auth/token', formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    });
    return response.data;
  },

  register: async (data: RegisterForm) => {
    const response = await api.post('/users/', data);
    return response.data;
  },

  forgetPassword: async (data: ForgetPasswordForm) => {
    const response = await api.post('/auth/forget', data);
    return response.data;
  },

  resetPassword: async (data: ResetPasswordForm) => {
    const response = await api.post('/auth/reset', data);
    return response.data;
  },

  getCurrentUser: async (): Promise<User> => {
    const response = await api.get('/users/me');
    return response.data;
  },
};

export const financeAPI = {
  // Incomes
  getIncomes: async (params?: {
    skip?: number;
    limit?: number;
    type_id?: number;
    start_date?: string;
    end_date?: string;
    project_id?: number;
  }): Promise<Income[]> => {
    const response = await api.get('/incomes/', { params });
    return response.data;
  },

  createIncome: async (data: IncomeForm): Promise<Income> => {
    const response = await api.post('/incomes/', data);
    return response.data;
  },

  updateIncome: async (id: number, data: IncomeForm): Promise<Income> => {
    const response = await api.put(`/incomes/${id}`, data);
    return response.data;
  },

  deleteIncome: async (id: number): Promise<void> => {
    await api.delete(`/incomes/${id}`);
  },

  // Expenses
  getExpenses: async (params?: {
    skip?: number;
    limit?: number;
    type_id?: number;
    start_date?: string;
    end_date?: string;
    project_id?: number;
  }): Promise<Expense[]> => {
    const response = await api.get('/expenses/', { params });
    return response.data;
  },

  createExpense: async (data: ExpenseForm): Promise<Expense> => {
    const response = await api.post('/expenses/', data);
    return response.data;
  },

  updateExpense: async (id: number, data: ExpenseForm): Promise<Expense> => {
    const response = await api.put(`/expenses/${id}`, data);
    return response.data;
  },

  deleteExpense: async (id: number): Promise<void> => {
    await api.delete(`/expenses/${id}`);
  },

  // Budgets
  getBudgets: async (params?: {
    skip?: number;
    limit?: number;
    project_id?: number;
  }): Promise<Budget[]> => {
    const response = await api.get('/budgets/', { params });
    return response.data;
  },

  createBudget: async (data: BudgetForm): Promise<Budget> => {
    const response = await api.post('/budgets/', data);
    return response.data;
  },

  updateBudget: async (id: number, data: BudgetForm): Promise<Budget> => {
    const response = await api.put(`/budgets/${id}`, data);
    return response.data;
  },

  deleteBudget: async (id: number): Promise<void> => {
    await api.delete(`/budgets/${id}`);
  },
};

export const projectAPI = {
  // Projects
  getProjects: async (params?: {
    skip?: number;
    limit?: number;
  }): Promise<Project[]> => {
    const response = await api.get('/projects/', { params });
    return response.data;
  },

  createProject: async (data: ProjectForm): Promise<Project> => {
    const response = await api.post('/projects/', data);
    return response.data;
  },

  deleteProject: async (id: number): Promise<void> => {
    await api.delete(`/projects/${id}`);
  },

  // Tasks
  getTasks: async (projectId: number): Promise<Task[]> => {
    const response = await api.get(`/tasks/${projectId}`);
    return response.data;
  },

  createTask: async (projectId: number, data: TaskForm): Promise<Task> => {
    const response = await api.post(`/tasks/${projectId}`, data);
    return response.data;
  },

  updateTask: async (projectId: number, taskId: number, data: TaskForm): Promise<Task> => {
    const response = await api.put(`/tasks/${projectId}/${taskId}`, data);
    return response.data;
  },

  deleteTask: async (projectId: number, taskId: number): Promise<void> => {
    await api.delete(`/tasks/${projectId}/${taskId}`);
  },
};

export const typesAPI = {
  // Income Types
  getIncomeTypes: async (): Promise<IncomeType[]> => {
    const response = await api.get('/types/income');
    return response.data;
  },

  createIncomeType: async (name: string): Promise<IncomeType> => {
    const response = await api.post('/types/income', { name });
    return response.data;
  },

  updateIncomeType: async (id: number, name: string): Promise<IncomeType> => {
    const response = await api.put(`/types/income/${id}`, { name });
    return response.data;
  },

  deleteIncomeType: async (id: number): Promise<void> => {
    await api.delete(`/types/income/${id}`);
  },

  // Expense Types
  getExpenseTypes: async (): Promise<ExpenseType[]> => {
    const response = await api.get('/types/expense');
    return response.data;
  },

  createExpenseType: async (name: string): Promise<ExpenseType> => {
    const response = await api.post('/types/expense', { name });
    return response.data;
  },

  updateExpenseType: async (id: number, name: string): Promise<ExpenseType> => {
    const response = await api.put(`/types/expense/${id}`, { name });
    return response.data;
  },

  deleteExpenseType: async (id: number): Promise<void> => {
    await api.delete(`/types/expense/${id}`);
  },

  // Budget Categories
  getBudgetCategories: async (): Promise<BudgetCategory[]> => {
    const response = await api.get('/types/budget');
    return response.data;
  },

  createBudgetCategory: async (name: string): Promise<BudgetCategory> => {
    const response = await api.post('/types/budget', { name });
    return response.data;
  },

  updateBudgetCategory: async (id: number, name: string): Promise<BudgetCategory> => {
    const response = await api.put(`/types/budget/${id}`, { name });
    return response.data;
  },

  deleteBudgetCategory: async (id: number): Promise<void> => {
    await api.delete(`/types/budget/${id}`);
  },
};

export const groupAPI = {
  // Groups
  getGroups: async (): Promise<Group[]> => {
    const response = await api.get('/groups/');
    return response.data;
  },

  createGroup: async (data: { name: string; description?: string }): Promise<Group> => {
    const response = await api.post('/groups/', data);
    return response.data;
  },

  deleteGroup: async (id: number): Promise<void> => {
    await api.delete(`/groups/${id}`);
  },

  addUserToGroup: async (groupId: number, userId: number): Promise<void> => {
    await api.post(`/groups/${groupId}/members/${userId}`);
  },

  // Group Shares
  getGroupShares: async (groupId: number): Promise<any[]> => {
    const response = await api.get(`/groups/${groupId}/shares`);
    return response.data;
  },

  createGroupShare: async (groupId: number, data: { user_id: number; permission: 'view' | 'edit' }): Promise<any> => {
    const response = await api.post(`/groups/${groupId}/shares`, data);
    return response.data;
  },

  deleteGroupShare: async (groupId: number, userId: number): Promise<void> => {
    await api.delete(`/groups/${groupId}/shares/${userId}`);
  },
};

export const analyticsAPI = {
  getFinancialSummary: async (groupId?: number): Promise<FinancialSummary> => {
    const params = groupId ? { group_id: groupId } : {};
    const response = await api.get('/analytics/summary', { params });
    return response.data;
  },
};

export default api;