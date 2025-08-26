// src/components/Finance/Incomes.tsx
import React, { useState, useEffect } from 'react';
import { useFinanceData } from '../../contexts/FinanceDataContext';
import IncomeForm from './IncomeForm';
import IncomeList from './IncomeList';
import { PlusIcon } from '@heroicons/react/24/outline';
import Button from '../Common/Button';

const Incomes: React.FC = () => {
  const { incomes, incomesLoading, fetchIncomes } = useFinanceData();
  const [showForm, setShowForm] = useState(false);
  const [editingIncome, setEditingIncome] = useState<any>(null);

  useEffect(() => {
    fetchIncomes();
  }, []);

  const handleEdit = (income: any) => {
    setEditingIncome(income);
    setShowForm(true);
  };

  const handleFormClose = () => {
    setShowForm(false);
    setEditingIncome(null);
  };

  if (incomesLoading) {
    return <div className="flex justify-center py-8">Loading incomes...</div>;
  }

  return (
    <div className="max-w-6xl mx-auto">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold text-gray-800">Income Management</h1>
        <Button onClick={() => setShowForm(true)}>
          <PlusIcon className="h-5 w-5 mr-2" />
          Add Income
        </Button>
      </div>

      <IncomeList incomes={incomes} onEdit={handleEdit} />

      {showForm && (
        <IncomeForm 
          income={editingIncome} 
          onClose={handleFormClose} 
          onSave={() => {
            handleFormClose();
            fetchIncomes();
          }}
        />
      )}
    </div>
  );
};

export default Incomes;