import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useParams } from 'react-router-dom';
import Modal from 'react-modal';

function TestDetails() {
  const { id } = useParams();
  const [test, setTest] = useState(null);
  const [modalIsOpen, setModalIsOpen] = useState(false);
  const [selectedImage, setSelectedImage] = useState(null);
  const [currentIndex, setCurrentIndex] = useState(0);

  useEffect(() => {
    const fetchTest = async () => {
      try {
        const response = await axios.get(`http://127.0.0.1:8080/tests/${id}`);
        setTest(response.data);
      } catch (error) {
        console.error('Error fetching test details', error);
      }
    };
    fetchTest();
  }, [id]);

  const openModal = (index) => {
    setCurrentIndex(index);
    setSelectedImage(test.image_tests[index].url);
    setModalIsOpen(true);
  };

  const closeModal = () => {
    setModalIsOpen(false);
    setSelectedImage(null);
  };

  const previousImage = () => {
    const newIndex = currentIndex === 0 ? test.image_tests.length - 1 : currentIndex - 1;
    setCurrentIndex(newIndex);
    setSelectedImage(test.image_tests[newIndex].url);
  };

  const nextImage = () => {
    const newIndex = currentIndex === test.image_tests.length - 1 ? 0 : currentIndex + 1;
    setCurrentIndex(newIndex);
    setSelectedImage(test.image_tests[newIndex].url);
  };

  if (!test) {
    return <div>Carregando...</div>;
  }

  return (
    <div className="bg-white p-8 rounded-lg shadow-lg max-w-4xl mx-auto">
      <h2 className="text-2xl font-bold mb-6 text-gray-800">Detalhes do Teste (ID: {test.id})</h2>
      <p><strong>URL:</strong> {test.url}</p>
      <p><strong>Nome do caso:</strong> {test.case_name}</p>
      <p>
        <strong>Status:</strong> 
        <span className={`ml-2 font-semibold ${test.status === 'success' ? 'text-green-500' : 'text-red-500'}`}>
          {test.status === 'success' ? 'Sucesso' : 'Falha'}
        </span>
      </p>
      <p><strong>Mensagens:</strong> {test.message}</p>
      <p><strong>Notas:</strong> {test.note}</p>
      <h3 className="text-lg font-bold mt-4">Testes de Imagem:</h3>
      <ul className="grid grid-cols-1 sm:grid-cols-2 gap-4 mt-4">
        {test.image_tests.map((image, index) => (
          <li key={index} className="border rounded-lg overflow-hidden shadow-sm">
            <img
              src={image.url}
              alt={`Screenshot ${index + 1}`}
              className="w-full h-auto cursor-pointer"
              onClick={() => openModal(index)}
            />
          </li>
        ))}
      </ul>

      <Modal
        isOpen={modalIsOpen}
        onRequestClose={closeModal}
        className="fixed inset-0 flex items-center justify-center p-4 bg-black bg-opacity-50 react-modal-overlay"
        overlayClassName="fixed inset-0 bg-black bg-opacity-50"
        shouldCloseOnOverlayClick={true}
      >
        {selectedImage && (
          <div className="relative flex items-center justify-center">
            <button
              onClick={previousImage}
              className="absolute left-2 text-white text-2xl z-10 bg-black bg-opacity-50 rounded-full p-2"
            >
              &#10094;
            </button>
            <img
              src={selectedImage}
              alt="Imagem ampliada"
              className="max-w-full max-h-screen"
              onClick={(e) => e.stopPropagation()} // Impede o fechamento ao clicar na imagem
            />
            <button
              onClick={nextImage}
              className="absolute right-2 text-white text-2xl z-10 bg-black bg-opacity-50 rounded-full p-2"
            >
              &#10095;
            </button>
            <button
              onClick={closeModal}
              className="absolute top-2 right-2 text-white text-xl"
            >
              &times;
            </button>
          </div>
        )}
      </Modal>
    </div>
  );
}

export default TestDetails;
