// src/pages/TestList.jsx
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';

function TestList() {
  const [tests, setTests] = useState([]);
  const [total, setTotal] = useState(0);
  const [limit] = useState(12);
  const [offset, setOffset] = useState(0);

  useEffect(() => {
    const fetchTests = async () => {
      try {
        const response = await axios.get(`http://127.0.0.1:8080/tests?limit=${limit}&offset=${offset}`);
        setTests(response.data.data);
        setTotal(response.data.total);
      } catch (error) {
        console.error('Error fetching tests', error);
      }
    };
    fetchTests();
  }, [offset]);

  const getStatusClass = (status) => {
    switch (status) {
      case 'success':
        return 'text-green-600 bg-green-100';
      case 'failure':
        return 'text-red-600 bg-red-100';
      default:
        return 'text-gray-600 bg-gray-100';
    }
  };

  return (
    <div className="bg-white p-8 rounded-lg shadow-lg max-w-6xl mx-auto">
      <h2 className="text-2xl font-bold mb-6 text-gray-800">Test List</h2>
      <table className="min-w-full bg-white border border-gray-200">
        <thead>
          <tr>
            <th className="py-2 px-4 border-b-2 border-gray-200 text-left text-gray-600 font-semibold">ID</th>
            <th className="py-2 px-4 border-b-2 border-gray-200 text-left text-gray-600 font-semibold">Case Name</th>
            <th className="py-2 px-4 border-b-2 border-gray-200 text-left text-gray-600 font-semibold">URL</th>
            <th className="py-2 px-4 border-b-2 border-gray-200 text-left text-gray-600 font-semibold">Status</th>
            <th className="py-2 px-4 border-b-2 border-gray-200 text-left text-gray-600 font-semibold">Message</th>
            <th className="py-2 px-4 border-b-2 border-gray-200 text-left text-gray-600 font-semibold">Details</th>
          </tr>
        </thead>
        <tbody>
          {tests.map((test) => (
            <tr key={test.id} className="hover:bg-gray-50">
              <td className="py-2 px-4 border-b border-gray-200">{test.id}</td>
              <td className="py-2 px-4 border-b border-gray-200">{test.case_name}</td>
              <td className="py-2 px-4 border-b border-gray-200">{test.url}</td>
              <td className="py-2 px-4 border-b border-gray-200">
                <span className={`py-1 px-3 rounded-full text-sm font-semibold ${getStatusClass(test.status)}`}>
                  {test.status}
                </span>
              </td>
              <td className="py-2 px-4 border-b border-gray-200">{test.message || 'N/A'}</td>
              <td className="py-2 px-4 border-b border-gray-200">
                <Link
                  to={`/tests/${test.id}`}
                  className="text-blue-600 font-semibold hover:underline"
                >
                  View Details
                </Link>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
      <div className="flex justify-between mt-6">
        <button
          onClick={() => setOffset(offset - limit)}
          disabled={offset === 0}
          className="bg-gray-300 text-gray-700 py-2 px-4 rounded disabled:opacity-50"
        >
          Previous
        </button>
        <button
          onClick={() => setOffset(offset + limit)}
          disabled={offset + limit >= total}
          className="bg-gray-300 text-gray-700 py-2 px-4 rounded disabled:opacity-50"
        >
          Next
        </button>
      </div>
    </div>
  );
}

export default TestList;
