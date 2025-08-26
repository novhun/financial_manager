// src/components/Finance/IncomeForm.tsx
import React, { useState, useEffect } from 'react';
import { useFinanceData } from '../../contexts/FinanceDataContext';
import { useModal } from '../../hooks/useModal';
import { Income, IncomeForm as IncomeFormType } from '../../types';

interface IncomeFormProps {
  income?: Income;
  onClose: () => void;
  onSave: () => void;
}

const IncomeForm: React.FC<IncomeFormProps> = ({ income, onClose, onSave }) => {
  const [formData, setFormData] = useState<IncomeFormType>({
    amount: 0,
    type_id: 0,
    description: '',
    date: new Date().toISOString().split('T')[0],
    group_id: undefined,
    project_id: undefined
  });
  const { createIncome, updateIncome, incomeTypes } = useFinanceData();
  const { openModal } = useModal();

  useEffect(() => {
    if (income) {
      setFormData({
        amount: income.amount,
        type_id: income.type_id,
        description: income.description || '',
        date: income.date ? income.date.split('T')[0] : new Date().toISOString().split('T')[0],
        group_id: income.group_id || undefined,
        project_id: income.project_id || undefined
      });
    }
  }, [income]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      if (income) {
        await updateIncome(income.id, formData);
      } else {
        await createIncome(formData);
      }
      onSave();
    } catch (error) {
      openModal(
        <p className="text-red-600">Failed to save income. Please try again.</p>,
        'Error'
      );
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: name === 'amount' ? parseFloat(value) || 0 : 
              name === 'type_id' || name === 'group_id' || name === 'project_id' ? 
              (value ? parseInt(value) : undefined) : value
    }));
  };

  return (
    <div className="fixed inset-0 bg-gray-600 bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg shadow-xl max-w-md w-full mx-4">
        <div className="px-6 py-4 border-b border-gray-200">
          <h3 className="text-lg font-semibold text-gray-900">
            {income ? 'Edit Income' : 'Add New Income'}
          </h3>
        </div>
        
        <form onSubmit={handleSubmit} className="px-6 py-4">
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Amount
              </label>
              <input
                type="number"
                name="amount"
                step="0.01"
                min="0"
                required
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                value={formData.amount}
                onChange={handleChange}
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Type
              </label>
              <select
                name="type_id"
                required
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                value={formData.type_id}
                onChange={handleChange}
              >
                <option value="">Select a type</option>
                {incomeTypes.map(type => (
                  <option key={type.id} value={type.id}>
                    {type.name}
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Description
              </label>
              <textarea
                name="description"
                rows={3}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                value={formData.description}
                onChange={handleChange}
                placeholder="Optional description"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Date
              </label>
              <input
                type="date"
                name="date"
                required
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                value={formData.date}
                onChange={handleChange}
              />
            </div>
          </div>

          <div className="mt-6 flex justify-end space-x-3">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 hover:bg-gray-200 rounded-md"
            >
              Cancel
            </button>
            <button
              type="submit"
              className="px-4 py-2 text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 rounded-md"
            >
              {income ? 'Update' : 'Create'} Income
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default IncomeForm;