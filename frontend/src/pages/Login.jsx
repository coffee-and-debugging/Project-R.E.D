
import { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import {jwtDecode} from 'jwt-decode';

export default function Login() {
  const [formData, setFormData] = useState({ email: '', password: '' });
  const navigate = useNavigate();

  const handleChange = e => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async e => {
    e.preventDefault();
    try {
      const res = await axios.post('http://localhost:8000/api/users/me/', formData);
      const token = res.data.token;
      localStorage.setItem('token', token);

      const user = jwtDecode(token);
      const role = user.role;

      navigate(`/${role}-dashboard`);
    } catch (err) {
      console.error('Registration error:', err.response?.data);
      alert('Login failed');
    }
  };

  return (
    <div className="max-w-md mx-auto mt-20 p-5 border shadow rounded">
      <h2 className="text-xl font-bold mb-4">Login</h2>
      <form onSubmit={handleSubmit} className="space-y-3">
        <input className="w-full p-2 border rounded" name="email" placeholder="Email" onChange={handleChange} required />
        <input type="password" className="w-full p-2 border rounded" name="password" placeholder="Password" onChange={handleChange} required />
        <button type="submit" className="w-full bg-red-600 text-white p-2 rounded">Login</button>
      </form>
    </div>
  );
}
