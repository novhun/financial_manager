// src/hooks/useModal.ts
import { useState, useCallback } from 'react';

export const useModal = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [modalContent, setModalContent] = useState<React.ReactNode>(null);
  const [modalTitle, setModalTitle] = useState('');

  const openModal = useCallback((content: React.ReactNode, title: string = '') => {
    setModalContent(content);
    setModalTitle(title);
    setIsOpen(true);
  }, []);

  const closeModal = useCallback(() => {
    setIsOpen(false);
    setModalContent(null);
    setModalTitle('');
  }, []);

  return {
    isOpen,
    modalContent,
    modalTitle,
    openModal,
    closeModal
  };
};