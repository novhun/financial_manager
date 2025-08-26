import React, { createContext, useState, useContext, ReactNode, useCallback } from 'react';
import { financeAPI, projectAPI, typesAPI, groupAPI, analyticsAPI } from '../services/api';
import { Income, Expense, Budget, Project, Task, IncomeType, ExpenseType, BudgetCategory, Group, FinancialSummary } from '../types';

interface FinanceDataContextType {
  // State
  incomes: Income[];
  expenses: Expense[];
  budgets: Budget[];
  projects: Project[];
  tasks: Record<number, Task[]>;
  incomeTypes: IncomeType[];
  expenseTypes: ExpenseType[];
  budgetCategories: BudgetCategory[];
  groups: Group[];
  financialSummary: FinancialSummary | null;
  
  // Loading states
  loading: boolean;
  incomesLoading: boolean;
  expensesLoading: boolean;
  budgetsLoading: boolean;
  projectsLoading: boolean;
  tasksLoading: boolean;
  typesLoading: boolean;
  groupsLoading: boolean;
  analyticsLoading: boolean;
  
  // Functions
  fetchIncomes: () => Promise<void>;
  fetchExpenses: () => Promise<void>;
  fetchBudgets: () => Promise<void>;
  fetchProjects: () => Promise<void>;
  fetchTasks: (projectId: number) => Promise<void>;
  fetchIncomeTypes: () => Promise<void>;
  fetchExpenseTypes: () => Promise<void>;
  fetchBudgetCategories: () => Promise<void>;
  fetchGroups: () => Promise<void>;
  fetchFinancialSummary: (groupId?: number) => Promise<void>;
  
  // CRUD operations
  createIncome: (data: any) => Promise<Income>;
  updateIncome: (id: number, data: any) => Promise<Income>;
  deleteIncome: (id: number) => Promise<void>;
  
  createExpense: (data: any) => Promise<Expense>;
  updateExpense: (id: number, data: any) => Promise<Expense>;
  deleteExpense: (id: number) => Promise<void>;
  
  createBudget: (data: any) => Promise<Budget>;
  updateBudget: (id: number, data: any) => Promise<Budget>;
  deleteBudget: (id: number) => Promise<void>;
  
  createProject: (data: any) => Promise<Project>;
  deleteProject: (id: number) => Promise<void>;
  
  createTask: (projectId: number, data: any) => Promise<Task>;
  updateTask: (projectId: number, taskId: number, data: any) => Promise<Task>;
  deleteTask: (projectId: number, taskId: number) => Promise<void>;
  
  createIncomeType: (name: string) => Promise<IncomeType>;
  updateIncomeType: (id: number, name: string) => Promise<IncomeType>;
  deleteIncomeType: (id: number) => Promise<void>;
  
  createExpenseType: (name: string) => Promise<ExpenseType>;
  updateExpenseType: (id: number, name: string) => Promise<ExpenseType>;
  deleteExpenseType: (id: number) => Promise<void>;
  
  createBudgetCategory: (name: string) => Promise<BudgetCategory>;
  updateBudgetCategory: (id: number, name: string) => Promise<BudgetCategory>;
  deleteBudgetCategory: (id: number) => Promise<void>;
  
  createGroup: (data: any) => Promise<Group>;
  deleteGroup: (id: number) => Promise<void>;
  addUserToGroup: (groupId: number, userId: number) => Promise<void>;
  createGroupShare: (groupId: number, data: any) => Promise<any>;
  deleteGroupShare: (groupId: number, userId: number) => Promise<void>;
}

const FinanceDataContext = createContext<FinanceDataContextType | undefined>(undefined);

export const useFinanceData = (): FinanceDataContextType => {
  const context = useContext(FinanceDataContext);
  if (context === undefined) {
    throw new Error('useFinanceData must be used within a FinanceDataProvider');
  }
  return context;
};

interface FinanceDataProviderProps {
  children: ReactNode;
}

export const FinanceDataProvider: React.FC<FinanceDataProviderProps> = ({ children }) => {
  // State
  const [incomes, setIncomes] = useState<Income[]>([]);
  const [expenses, setExpenses] = useState<Expense[]>([]);
  const [budgets, setBudgets] = useState<Budget[]>([]);
  const [projects, setProjects] = useState<Project[]>([]);
  const [tasks, setTasks] = useState<Record<number, Task[]>>({});
  const [incomeTypes, setIncomeTypes] = useState<IncomeType[]>([]);
  const [expenseTypes, setExpenseTypes] = useState<ExpenseType[]>([]);
  const [budgetCategories, setBudgetCategories] = useState<BudgetCategory[]>([]);
  const [groups, setGroups] = useState<Group[]>([]);
  const [financialSummary, setFinancialSummary] = useState<FinancialSummary | null>(null);
  
  // Loading states
  const [loading, setLoading] = useState(false);
  const [incomesLoading, setIncomesLoading] = useState(false);
  const [expensesLoading, setExpensesLoading] = useState(false);
  const [budgetsLoading, setBudgetsLoading] = useState(false);
  const [projectsLoading, setProjectsLoading] = useState(false);
  const [tasksLoading, setTasksLoading] = useState(false);
  const [typesLoading, setTypesLoading] = useState(false);
  const [groupsLoading, setGroupsLoading] = useState(false);
  const [analyticsLoading, setAnalyticsLoading] = useState(false);

  // Fetch functions with useCallback to avoid dependency issues
  const fetchIncomes = useCallback(async () => {
    setIncomesLoading(true);
    try {
      const data = await financeAPI.getIncomes();
      setIncomes(data);
    } catch (error) {
      console.error('Failed to fetch incomes:', error);
    } finally {
      setIncomesLoading(false);
    }
  }, []);

  const fetchExpenses = useCallback(async () => {
    setExpensesLoading(true);
    try {
      const data = await financeAPI.getExpenses();
      setExpenses(data);
    } catch (error) {
      console.error('Failed to fetch expenses:', error);
    } finally {
      setExpensesLoading(false);
    }
  }, []);

  const fetchBudgets = useCallback(async () => {
    setBudgetsLoading(true);
    try {
      const data = await financeAPI.getBudgets();
      setBudgets(data);
    } catch (error) {
      console.error('Failed to fetch budgets:', error);
    } finally {
      setBudgetsLoading(false);
    }
  }, []);

  const fetchProjects = useCallback(async () => {
    setProjectsLoading(true);
    try {
      const data = await projectAPI.getProjects();
      setProjects(data);
    } catch (error) {
      console.error('Failed to fetch projects:', error);
    } finally {
      setProjectsLoading(false);
    }
  }, []);

  const fetchTasks = useCallback(async (projectId: number) => {
    setTasksLoading(true);
    try {
      const data = await projectAPI.getTasks(projectId);
      setTasks(prev => ({ ...prev, [projectId]: data }));
    } catch (error) {
      console.error('Failed to fetch tasks:', error);
    } finally {
      setTasksLoading(false);
    }
  }, []);

  const fetchIncomeTypes = useCallback(async () => {
    setTypesLoading(true);
    try {
      const data = await typesAPI.getIncomeTypes();
      setIncomeTypes(data);
    } catch (error) {
      console.error('Failed to fetch income types:', error);
    } finally {
      setTypesLoading(false);
    }
  }, []);

  const fetchExpenseTypes = useCallback(async () => {
    setTypesLoading(true);
    try {
      const data = await typesAPI.getExpenseTypes();
      setExpenseTypes(data);
    } catch (error) {
      console.error('Failed to fetch expense types:', error);
    } finally {
      setTypesLoading(false);
    }
  }, []);

  const fetchBudgetCategories = useCallback(async () => {
    setTypesLoading(true);
    try {
      const data = await typesAPI.getBudgetCategories();
      setBudgetCategories(data);
    } catch (error) {
      console.error('Failed to fetch budget categories:', error);
    } finally {
      setTypesLoading(false);
    }
  }, []);

  const fetchGroups = useCallback(async () => {
    setGroupsLoading(true);
    try {
      const data = await groupAPI.getGroups();
      setGroups(data);
    } catch (error) {
      console.error('Failed to fetch groups:', error);
    } finally {
      setGroupsLoading(false);
    }
  }, []);

  const fetchFinancialSummary = useCallback(async (groupId?: number) => {
    setAnalyticsLoading(true);
    try {
      const data = await analyticsAPI.getFinancialSummary(groupId);
      setFinancialSummary(data);
    } catch (error) {
      console.error('Failed to fetch financial summary:', error);
    } finally {
      setAnalyticsLoading(false);
    }
  }, []);

  // CRUD operations
  const createIncome = async (data: any): Promise<Income> => {
    const newIncome = await financeAPI.createIncome(data);
    setIncomes(prev => [...prev, newIncome]);
    return newIncome;
  };

  const updateIncome = async (id: number, data: any): Promise<Income> => {
    const updatedIncome = await financeAPI.updateIncome(id, data);
    setIncomes(prev => prev.map(income => income.id === id ? updatedIncome : income));
    return updatedIncome;
  };

  const deleteIncome = async (id: number): Promise<void> => {
    await financeAPI.deleteIncome(id);
    setIncomes(prev => prev.filter(income => income.id !== id));
  };

  // Similar CRUD operations for other entities...

  const value: FinanceDataContextType = {
    // State
    incomes,
    expenses,
    budgets,
    projects,
    tasks,
    incomeTypes,
    expenseTypes,
    budgetCategories,
    groups,
    financialSummary,
    
    // Loading states
    loading,
    incomesLoading,
    expensesLoading,
    budgetsLoading,
    projectsLoading,
    tasksLoading,
    typesLoading,
    groupsLoading,
    analyticsLoading,
    
    // Fetch functions
    fetchIncomes,
    fetchExpenses,
    fetchBudgets,
    fetchProjects,
    fetchTasks,
    fetchIncomeTypes,
    fetchExpenseTypes,
    fetchBudgetCategories,
    fetchGroups,
    fetchFinancialSummary,
    
    // CRUD operations
    createIncome,
    updateIncome,
    deleteIncome,
    
    createExpense: async (data: any) => {
      const newExpense = await financeAPI.createExpense(data);
      setExpenses(prev => [...prev, newExpense]);
      return newExpense;
    },
    
    updateExpense: async (id: number, data: any) => {
      const updatedExpense = await financeAPI.updateExpense(id, data);
      setExpenses(prev => prev.map(expense => expense.id === id ? updatedExpense : expense));
      return updatedExpense;
    },
    
    deleteExpense: async (id: number) => {
      await financeAPI.deleteExpense(id);
      setExpenses(prev => prev.filter(expense => expense.id !== id));
    },
    
    createBudget: async (data: any) => {
      const newBudget = await financeAPI.createBudget(data);
      setBudgets(prev => [...prev, newBudget]);
      return newBudget;
    },
    
    updateBudget: async (id: number, data: any) => {
      const updatedBudget = await financeAPI.updateBudget(id, data);
      setBudgets(prev => prev.map(budget => budget.id === id ? updatedBudget : budget));
      return updatedBudget;
    },
    
    deleteBudget: async (id: number) => {
      await financeAPI.deleteBudget(id);
      setBudgets(prev => prev.filter(budget => budget.id !== id));
    },
    
    createProject: async (data: any) => {
      const newProject = await projectAPI.createProject(data);
      setProjects(prev => [...prev, newProject]);
      return newProject;
    },
    
    deleteProject: async (id: number) => {
      await projectAPI.deleteProject(id);
      setProjects(prev => prev.filter(project => project.id !== id));
    },
    
    createTask: async (projectId: number, data: any) => {
      const newTask = await projectAPI.createTask(projectId, data);
      setTasks(prev => ({
        ...prev,
        [projectId]: [...(prev[projectId] || []), newTask]
      }));
      return newTask;
    },
    
    updateTask: async (projectId: number, taskId: number, data: any) => {
      const updatedTask = await projectAPI.updateTask(projectId, taskId, data);
      setTasks(prev => ({
        ...prev,
        [projectId]: (prev[projectId] || []).map(task => 
          task.id === taskId ? updatedTask : task
        )
      }));
      return updatedTask;
    },
    
    deleteTask: async (projectId: number, taskId: number) => {
      await projectAPI.deleteTask(projectId, taskId);
      setTasks(prev => ({
        ...prev,
        [projectId]: (prev[projectId] || []).filter(task => task.id !== taskId)
      }));
    },
    
    createIncomeType: async (name: string) => {
      const newType = await typesAPI.createIncomeType(name);
      setIncomeTypes(prev => [...prev, newType]);
      return newType;
    },
    
    updateIncomeType: async (id: number, name: string) => {
      const updatedType = await typesAPI.updateIncomeType(id, name);
      setIncomeTypes(prev => prev.map(type => type.id === id ? updatedType : type));
      return updatedType;
    },
    
    deleteIncomeType: async (id: number) => {
      await typesAPI.deleteIncomeType(id);
      setIncomeTypes(prev => prev.filter(type => type.id !== id));
    },
    
    createExpenseType: async (name: string) => {
      const newType = await typesAPI.createExpenseType(name);
      setExpenseTypes(prev => [...prev, newType]);
      return newType;
    },
    
    updateExpenseType: async (id: number, name: string) => {
      const updatedType = await typesAPI.updateExpenseType(id, name);
      setExpenseTypes(prev => prev.map(type => type.id === id ? updatedType : type));
      return updatedType;
    },
    
    deleteExpenseType: async (id: number) => {
      await typesAPI.deleteExpenseType(id);
      setExpenseTypes(prev => prev.filter(type => type.id !== id));
    },
    
    createBudgetCategory: async (name: string) => {
      const newCategory = await typesAPI.createBudgetCategory(name);
      setBudgetCategories(prev => [...prev, newCategory]);
      return newCategory;
    },
    
    updateBudgetCategory: async (id: number, name: string) => {
      const updatedCategory = await typesAPI.updateBudgetCategory(id, name);
      setBudgetCategories(prev => prev.map(category => category.id === id ? updatedCategory : category));
      return updatedCategory;
    },
    
    deleteBudgetCategory: async (id: number) => {
      await typesAPI.deleteBudgetCategory(id);
      setBudgetCategories(prev => prev.filter(category => category.id !== id));
    },
    
    createGroup: async (data: any) => {
      const newGroup = await groupAPI.createGroup(data);
      setGroups(prev => [...prev, newGroup]);
      return newGroup;
    },
    
    deleteGroup: async (id: number) => {
      await groupAPI.deleteGroup(id);
      setGroups(prev => prev.filter(group => group.id !== id));
    },
    
    addUserToGroup: async (groupId: number, userId: number) => {
      await groupAPI.addUserToGroup(groupId, userId);
      await fetchGroups();
    },
    
    createGroupShare: async (groupId: number, data: any) => {
      return await groupAPI.createGroupShare(groupId, data);
    },
    
    deleteGroupShare: async (groupId: number, userId: number) => {
      await groupAPI.deleteGroupShare(groupId, userId);
    }
  };

  return (
    <FinanceDataContext.Provider value={value}>
      {children}
    </FinanceDataContext.Provider>
  );
};