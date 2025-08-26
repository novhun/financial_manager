// src/components/Finance/Expenses.tsx
import React, { useState, useEffect } from 'react';
import { useFinanceData } from '../../contexts/FinanceDataContext';
import ExpenseForm from './ExpenseForm';
import ExpenseList from './ExpenseList';
import { PlusIcon } from '@heroicons/react/24/outline';
import Button from '../Common/Button';

const Expenses: React.FC = () => {
  const { expenses, expensesLoading, fetchExpenses } = useFinanceData();
  const [showForm, setShowForm] = useState(false);
  const [editingExpense, setEditingExpense] = useState<any>(null);

  useEffect(() => {
    fetchExpenses();
  }, []);

  const handleEdit = (expense: any) => {
    setEditingExpense(expense);
    setShowForm(true);
  };

  const handleFormClose = () => {
    setShowForm(false);
    setEditingExpense(null);
  };

  if (expensesLoading) {
    return <div className="flex justify-center py-8">Loading expenses...</div>;
  }

  return (
    <div className="max-w-6xl mx-auto">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold text-gray-800">Expense Management</h1>
        <Button onClick={() => setShowForm(true)}>
          <PlusIcon className="h-5 w-5 mr-2" />
          Add Expense
        </Button>
      </div>

      <ExpenseList expenses={expenses} onEdit={handleEdit} />

      {showForm && (
        <ExpenseForm 
          expense={editingExpense} 
          onClose={handleFormClose} 
          onSave={() => {
            handleFormClose();
            fetchExpenses();
          }}
        />
      )}
    </div>
  );
};

export default Expenses;