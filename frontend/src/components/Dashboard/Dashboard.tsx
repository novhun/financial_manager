import React, { useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useFinanceData } from '../../contexts/FinanceDataContext';
import { useLoading } from '../../hooks/useLoading';
import {
  CurrencyDollarIcon,
  ChartBarIcon,
  ClipboardListIcon
} from '@heroicons/react/24/outline';

const Dashboard: React.FC = () => {
  const { 
    financialSummary, 
    incomes, 
    expenses, 
    projects, 
    fetchFinancialSummary, 
    fetchIncomes, 
    fetchExpenses, 
    fetchProjects 
  } = useFinanceData();
  const { startLoading, stopLoading } = useLoading();

  useEffect(() => {
    const loadData = async () => {
      startLoading();
      try {
        await Promise.all([
          fetchFinancialSummary(),
          fetchIncomes(),
          fetchExpenses(),
          fetchProjects()
        ]);
      } catch (error) {
        console.error('Failed to load dashboard data:', error);
      } finally {
        stopLoading();
      }
    };

    loadData();
  }, [fetchFinancialSummary, fetchIncomes, fetchExpenses, fetchProjects, startLoading, stopLoading]);

  const stats = [
    {
      name: 'Total Income',
      value: `$${financialSummary?.total_income?.toFixed(2) || '0.00'}`,
      icon: CurrencyDollarIcon,
      color: 'text-green-600',
      bgColor: 'bg-green-100',
      href: '/incomes'
    },
    {
      name: 'Total Expenses',
      value: `$${financialSummary?.total_expense?.toFixed(2) || '0.00'}`,
      icon: CurrencyDollarIcon,
      color: 'text-red-600',
      bgColor: 'bg-red-100',
      href: '/expenses'
    },
    {
      name: 'Net Balance',
      value: `$${financialSummary?.net_balance?.toFixed(2) || '0.00'}`,
      icon: ChartBarIcon,
      color: financialSummary?.net_balance && financialSummary.net_balance >= 0 ? 'text-green-600' : 'text-red-600',
      bgColor: financialSummary?.net_balance && financialSummary.net_balance >= 0 ? 'bg-green-100' : 'bg-red-100',
      href: '/analytics'
    },
    {
      name: 'Active Projects',
      value: projects.length.toString(),
      icon: ClipboardListIcon,
      color: 'text-blue-600',
      bgColor: 'bg-blue-100',
      href: '/projects'
    }
  ];

  const recentTransactions = [...incomes, ...expenses]
    .sort((a, b) => new Date(b.date || '').getTime() - new Date(a.date || '').getTime())
    .slice(0, 5);

  return (
    <div className="max-w-7xl mx-auto">
      <h1 className="text-2xl font-bold text-gray-800 mb-6">Dashboard</h1>
      
      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        {stats.map((stat) => {
          const Icon = stat.icon;
          return (
            <Link
              key={stat.name}
              to={stat.href}
              className="bg-white overflow-hidden shadow rounded-lg hover:shadow-md transition-shadow"
            >
              <div className="p-5">
                <div className="flex items-center">
                  <div className={`flex-shrink-0 rounded-md p-3 ${stat.bgColor}`}>
                    <Icon className={`h-6 w-6 ${stat.color}`} />
                  </div>
                  <div className="ml-5 w-0 flex-1">
                    <dl>
                      <dt className="text-sm font-medium text-gray-500 truncate">
                        {stat.name}
                      </dt>
                      <dd className={`text-lg font-semibold ${stat.color}`}>
                        {stat.value}
                      </dd>
                    </dl>
                  </div>
                </div>
              </div>
            </Link>
          );
        })}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Recent Transactions */}
        <div className="bg-white shadow rounded-lg">
          <div className="px-4 py-5 sm:px-6 border-b border-gray-200">
            <h3 className="text-lg font-medium leading-6 text-gray-900">Recent Transactions</h3>
          </div>
          <div className="px-4 py-5 sm:p-6">
            <ul className="divide-y divide-gray-200">
              {recentTransactions.length > 0 ? (
                recentTransactions.map((transaction) => (
                  <li key={transaction.id} className="py-3">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center">
                        <div className={`p-2 rounded-md ${
                          'type_id' in transaction ? 'bg-green-100' : 'bg-red-100'
                        }`}>
                          <CurrencyDollarIcon className={`h-5 w-5 ${
                            'type_id' in transaction ? 'text-green-600' : 'text-red-600'
                          }`} />
                        </div>
                        <div className="ml-4">
                          <p className="text-sm font-medium text-gray-900">
                            {transaction.description || 'No description'}
                          </p>
                          <p className="text-sm text-gray-500">
                            {transaction.date ? new Date(transaction.date).toLocaleDateString() : 'No date'}
                          </p>
                        </div>
                      </div>
                      <p className={`text-sm font-semibold ${
                        'type_id' in transaction ? 'text-green-600' : 'text-red-600'
                      }`}>
                        {'type_id' in transaction ? '+' : '-'}${transaction.amount.toFixed(2)}
                      </p>
                    </div>
                  </li>
                ))
              ) : (
                <li className="py-4 text-center text-gray-500">
                  No transactions yet
                </li>
              )}
            </ul>
          </div>
        </div>

        {/* Quick Actions */}
        <div className="bg-white shadow rounded-lg">
          <div className="px-4 py-5 sm:px-6 border-b border-gray-200">
            <h3 className="text-lg font-medium leading-6 text-gray-900">Quick Actions</h3>
          </div>
          <div className="px-4 py-5 sm:p-6">
            <div className="grid grid-cols-2 gap-4">
              <Link
                to="/incomes"
                className="flex flex-col items-center p-4 border border-gray-200 rounded-lg hover:bg-gray-50"
              >
                <CurrencyDollarIcon className="h-8 w-8 text-green-600 mb-2" />
                <span className="text-sm font-medium text-gray-900">Add Income</span>
              </Link>
              <Link
                to="/expenses"
                className="flex flex-col items-center p-4 border border-gray-200 rounded-lg hover:bg-gray-50"
              >
                <CurrencyDollarIcon className="h-8 w-8 text-red-600 mb-2" />
                <span className="text-sm font-medium text-gray-900">Add Expense</span>
              </Link>
              <Link
                to="/projects"
                className="flex flex-col items-center p-4 border border-gray-200 rounded-lg hover:bg-gray-50"
              >
                <ClipboardListIcon className="h-8 w-8 text-blue-600 mb-2" />
                <span className="text-sm font-medium text-gray-900">Create Project</span>
              </Link>
              <Link
                to="/budgets"
                className="flex flex-col items-center p-4 border border-gray-200 rounded-lg hover:bg-gray-50"
              >
                <ChartBarIcon className="h-8 w-8 text-purple-600 mb-2" />
                <span className="text-sm font-medium text-gray-900">Set Budget</span>
              </Link>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;