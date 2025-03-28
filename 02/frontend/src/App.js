import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [books, setBooks] = useState([]);
  const [randomUser, setRandomUser] = useState(null);
  const [loans, setLoans] = useState([]);

  const fetchBooks = async () => {
    try {
      const response = await fetch('http://localhost:5000/api/books');
      const data = await response.json();
      setBooks(data);
    } catch (error) {
      console.error("Error fetching books:", error);
    }
  };

  const generateRandomUser = async () => {
    try {
      const response = await fetch('http://localhost:5000/api/users/random');
      const data = await response.json();
      setRandomUser(data);
    } catch (error) {
      console.error("Error generating user:", error);
    }
  };

  const fetchLoans = async () => {
    try {
      const response = await fetch('http://localhost:5000/api/loans');
      const data = await response.json();
      setLoans(data);
    } catch (error) {
      console.error("Error fetching loans:", error);
    }
  };

  return (
    <div className="App">
      <h1>Library Management System</h1>

      <section>
        <h2>Books</h2>
        <button onClick={fetchBooks}>Load Books</button>
        <div className="book-list">
          {books.map(book => (
            <div key={book.id} className="book-card">
              {book.cover && <img src={book.cover} alt={book.name} />}
              <h3>{book.name}</h3>
              <p>Author: {book.author}</p>
              <p>Genre: {book.genre}</p>
            </div>
          ))}
        </div>
      </section>

      <section>
        <h2>Generate Random User</h2>
        <button onClick={generateRandomUser}>Generate User</button>
        {randomUser && (
          <div className="user-card">
            <h3>New User Added</h3>
            <p>Name: {randomUser.name}</p>
            <p>Email: {randomUser.email}</p>
          </div>
        )}
      </section>

      <section>
        <h2>Loans</h2>
        <button onClick={fetchLoans}>Load Loans</button>
        <div className="loan-list">
          {loans.map(loan => (
            <div key={loan.id} className="loan-card">
              <h3>Loan #{loan.id}</h3>
              <p>User: {loan.user?.name} ({loan.user?.email})</p>
              <p>Book: {loan.book?.name} by {loan.book?.author}</p>
              <p>Loan Date: {loan.loan_date}</p>
              <p>Return Date: {loan.return_date || "Not returned"}</p>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}

export default App;