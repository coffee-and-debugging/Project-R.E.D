
import { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

export default function Register() {
  const [formData, setFormData] = useState({
    username: '', email: '', password: '', role: 'donor'
  });
  const navigate = useNavigate();

  const handleChange = e => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async e => {
    e.preventDefault();
    try {
      await axios.post('http://localhost:8000/api/users/register/', formData);
      alert('Registration successful');
      navigate('/login');
    } catch (err) {
      alert('Registration failed');
    }
  };

  return (
    <div className="max-w-md mx-auto mt-20 p-5 border shadow rounded">
      <h2 className="text-xl font-bold mb-4">Register</h2>
      <form onSubmit={handleSubmit} className="space-y-3">
        <input className="w-full p-2 border rounded" name="username" placeholder="Username" onChange={handleChange} required />
        <input className="w-full p-2 border rounded" name="email" placeholder="Email" onChange={handleChange} required />
        <input type="password" className="w-full p-2 border rounded" name="password" placeholder="Password" onChange={handleChange} required />
        <select name="role" onChange={handleChange} className="w-full p-2 border rounded">
          <option value="donor">Donor</option>
          <option value="patient">Patient</option>
          <option value="hospital">Hospital</option>
          <option value="admin">Admin</option>
        </select>
        <input className="w-full p-2 border rounded" name="bloodgroup" placeholder="Blood Group" onChange={handleChange} required />
        <input className="w-full p-2 border rounded" name="age" placeholder="Age" onChange={handleChange} required />
        <input className="w-full p-2 border rounded" name="phone" placeholder="Phone Number" onChange={handleChange} required />
        <input className="w-full p-2 border rounded" name="address" placeholder="Address" onChange={handleChange} required />
        <input className="w-full p-2 border rounded" name="allergies" placeholder="Allergies" onChange={handleChange} required />
        <button type="submit" className="w-full bg-red-600 text-white p-2 rounded">Register</button>
      </form>
    </div>
  );
}
