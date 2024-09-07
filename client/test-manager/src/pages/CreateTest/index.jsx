import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const elementTypes = [
  { label: 'Class Name', value: 'class_name' },
  { label: 'ID', value: 'id' },
  { label: 'Name', value: 'name' },
  { label: 'XPath', value: 'xpath' },
  { label: 'CSS Selector', value: 'css_selector' },
  { label: 'Tag Name', value: 'tag_name' },
  { label: 'Link Text', value: 'link_text' },
  { label: 'Partial Link Text', value: 'partial_link_text' },
];

const actionTypes = [
  { label: 'Input Text', value: 'input' },
  { label: 'Click', value: 'click' },
];

const initialCase = {
  name: '',
  steps: [
    {
      id: `${Date.now()}`,
      type: 'name',
      element: '',
      action_type: 'input',
      value: '',
      validations_field: { message: '' },
    },
  ],
};

function CreateTest() {
  const [url, setUrl] = useState('');
  const [testCases, setTestCases] = useState([initialCase]);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate(); // Hook for navigation

  const handleStepChange = (caseIndex, stepIndex, key, value) => {
    const newTestCases = [...testCases];
    newTestCases[caseIndex].steps[stepIndex][key] = value;
    setTestCases(newTestCases);
  };

  const handleCaseChange = (caseIndex, key, value) => {
    const newTestCases = [...testCases];
    newTestCases[caseIndex][key] = value;
    setTestCases(newTestCases);
  };

  const addNewStep = (caseIndex) => {
    const newTestCases = [...testCases];
    newTestCases[caseIndex].steps.push({
      id: `${Date.now()}`,
      type: 'name',
      element: '',
      action_type: 'input',
      value: '',
      validations_field: { message: '' },
    });
    setTestCases(newTestCases);
  };

  const removeStep = (caseIndex, stepIndex) => {
    const newTestCases = [...testCases];
    newTestCases[caseIndex].steps.splice(stepIndex, 1);
    setTestCases(newTestCases);
  };

  const addNewCase = () => {
    setTestCases([...testCases, { ...initialCase, name: `Test Case ${testCases.length + 1}` }]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      await axios.post('http://127.0.0.1:8080/tests', { url, cases: testCases });
      alert('Test created successfully!');
      navigate('/');
    } catch (error) {
      console.error('There was an error creating the test!', error);
    } finally {
      setLoading(false); 
    }
  };

  return (
    <div className="bg-white p-8 rounded-lg shadow-lg max-w-4xl mx-auto">
      <h2 className="text-2xl font-bold mb-6 text-gray-800">Criação de novo teste</h2>
      <form onSubmit={handleSubmit}>
        <div className="mb-6">
          <label className="block text-gray-700 font-semibold mb-2">URL:</label>
          <input
            type="text"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            className="w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="Enter the test URL"
            required
          />
        </div>
        {testCases.map((testCase, caseIndex) => (
          <div key={caseIndex} className="mb-8 bg-gray-50 p-4 rounded-lg border border-gray-200">
            <div className="mb-4">
              <label className="block text-gray-700 font-semibold mb-2">Nome do caso:</label>
              <input
                type="text"
                value={testCase.name}
                onChange={(e) => handleCaseChange(caseIndex, 'name', e.target.value)}
                className="w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Enter the case name"
                required
              />
            </div>
            {testCase.steps.map((step, stepIndex) => (
              <div key={step.id} className="p-4 bg-gray-100 border border-gray-300 rounded-md shadow-sm mb-4">
                <div className="flex justify-between items-center mb-2">
                  <label className="font-semibold text-gray-700 mr-2">
                    Step {stepIndex + 1}:
                  </label>
                  <div className="flex-grow">
                    <select
                      value={step.type}
                      onChange={(e) => handleStepChange(caseIndex, stepIndex, 'type', e.target.value)}
                      className="mr-2 px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    >
                      {elementTypes.map((option) => (
                        <option key={option.value} value={option.value}>
                          {option.label}
                        </option>
                      ))}
                    </select>
                    <input
                      type="text"
                      value={step.element}
                      onChange={(e) => handleStepChange(caseIndex, stepIndex, 'element', e.target.value)}
                      className="px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                      placeholder="Enter element"
                    />
                  </div>
                </div>
                <div className="mt-2 text-sm text-gray-600">
                  <label className="font-semibold text-gray-700">Action Type:</label>
                  <select
                    value={step.action_type}
                    onChange={(e) => handleStepChange(caseIndex, stepIndex, 'action_type', e.target.value)}
                    className="w-full mt-2 px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  >
                    {actionTypes.map((option) => (
                      <option key={option.value} value={option.value}>
                        {option.label}
                      </option>
                    ))}
                  </select>
                </div>
                {step.action_type === 'input' && (
                  <div className="mt-2 text-sm text-gray-600">
                    <label className="font-semibold text-gray-700">Value:</label>
                    <input
                      type="text"
                      value={step.value}
                      onChange={(e) => handleStepChange(caseIndex, stepIndex, 'value', e.target.value)}
                      className="w-full mt-2 px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                      placeholder="Enter value"
                    />
                  </div>
                )}
                <div className="mt-2 text-sm text-gray-600">
                  <label className="font-semibold text-gray-700">Validation Message:</label>
                  <input
                    type="text"
                    value={step.validations_field.message}
                    onChange={(e) => handleStepChange(caseIndex, stepIndex, 'validations_field', {
                      ...step.validations_field,
                      message: e.target.value,
                    })}
                    className="w-full mt-2 px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    placeholder="Enter validation message"
                  />
                </div>
                <button
                  type="button"
                  onClick={() => removeStep(caseIndex, stepIndex)}
                  className="mt-4 bg-red-500 text-white py-2 px-4 rounded-md font-semibold hover:bg-red-600 transition"
                >
                  Remover passo
                </button>
              </div>
            ))}
            <button
              type="button"
              onClick={() => addNewStep(caseIndex)}
              className="mt-4 bg-green-500 text-white py-2 px-4 rounded-md font-semibold hover:bg-green-600 transition"
            >
              Add passo
            </button>
          </div>
        ))}
        <button
          type="button"
          onClick={addNewCase}
          className="mt-4 bg-blue-500 text-white py-2 px-4 rounded-md font-semibold hover:bg-blue-600 transition"
        >
          Add novo caso
        </button>
        <button
          type="submit"
          className="mt-6 w-full bg-blue-600 text-white py-3 rounded-md font-semibold hover:bg-blue-700 transition"
          disabled={loading}
        >
          {loading ? (
            <div className="flex justify-center items-center">
              <div className="loader ease-linear rounded-full border-4 border-t-4 border-gray-200 h-6 w-6 mr-2"></div>
              Creating Test...
            </div>
          ) : (
            'Criar no teste'
          )}
        </button>
      </form>
    </div>
  );
}

// Loader CSS (This can be added in your CSS file)
const style = document.createElement('style');
style.innerHTML = `
  .loader {
    border-top-color: #3498db;
    animation: spinner 0.6s linear infinite;
  }

  @keyframes spinner {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }
`;
document.head.appendChild(style);

export default CreateTest;
