// src/components/Finance/IncomeList.tsx
import React from 'react';
import { PencilIcon, TrashIcon } from '@heroicons/react/24/outline';
import { useFinanceData } from '../../contexts/FinanceDataContext';
import { useModal } from '../../hooks/useModal';
import { Income } from '../../types';

interface IncomeListProps {
  incomes: Income[];
  onEdit: (income: Income) => void;
}

const IncomeList: React.FC<IncomeListProps> = ({ incomes, onEdit }) => {
  const { deleteIncome, incomeTypes } = useFinanceData();
  const { openModal } = useModal();

  const handleDelete = async (income: Income) => {
    openModal(
      <div>
        <p className="text-gray-700 mb-4">
          Are you sure you want to delete this income of ${income.amount}?
        </p>
        <div className="flex justify-end space-x-3">
          <button
            onClick={() => useModal.getState().closeModal()}
            className="px-4 py-2 text-sm text-gray-700 bg-gray-100 hover:bg-gray-200 rounded-md"
          >
            Cancel
          </button>
          <button
            onClick={async () => {
              try {
                await deleteIncome(income.id);
                useModal.getState().closeModal();
              } catch (error) {
                openModal(
                  <p className="text-red-600">Failed to delete income. Please try again.</p>,
                  'Error'
                );
              }
            }}
            className="px-4 py-2 text-sm text-white bg-red-600 hover:bg-red-700 rounded-md"
          >
            Delete
          </button>
        </div>
      </div>,
      'Confirm Deletion'
    );
  };

  const getTypeName = (typeId: number) => {
    const type = incomeTypes.find(t => t.id === typeId);
    return type?.name || 'Unknown';
  };

  if (incomes.length === 0) {
    return (
      <div className="bg-white shadow rounded-lg p-6 text-center">
        <CurrencyDollarIcon className="h-12 w-12 text-gray-400 mx-auto mb-4" />
        <h3 className="text-lg font-medium text-gray-900 mb-2">No incomes yet</h3>
        <p className="text-gray-500">Get started by adding your first income.</p>
      </div>
    );
  }

  return (
    <div className="bg-white shadow rounded-lg overflow-hidden">
      <div className="px-4 py-5 sm:px-6 border-b border-gray-200">
        <h3 className="text-lg font-medium leading-6 text-gray-900">Income Records</h3>
      </div>
      <ul className="divide-y divide-gray-200">
        {incomes.map((income) => (
          <li key={income.id} className="px-4 py-4 sm:px-6">
            <div className="flex items-center justify-between">
              <div className="flex items-center">
                <div className="bg-green-100 p-2 rounded-md">
                  <CurrencyDollarIcon className="h-5 w-5 text-green-600" />
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-900">
                    {getTypeName(income.type_id)}
                  </p>
                  <p className="text-sm text-gray-500">
                    {income.description || 'No description'}
                  </p>
                  <p className="text-xs text-gray-400">
                    {income.date ? new Date(income.date).toLocaleDateString() : 'No date'}
                  </p>
                </div>
              </div>
              
              <div className="flex items-center space-x-2">
                <span className="text-sm font-semibold text-green-600">
                  ${income.amount.toFixed(2)}
                </span>
                
                <button
                  onClick={() => onEdit(income)}
                  className="text-blue-600 hover:text-blue-800 p-1"
                >
                  <PencilIcon className="h-4 w-4" />
                </button>
                
                <button
                  onClick={() => handleDelete(income)}
                  className="text-red-600 hover:text-red-800 p-1"
                >
                  <TrashIcon className="h-4 w-4" />
                </button>
              </div>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default IncomeList;