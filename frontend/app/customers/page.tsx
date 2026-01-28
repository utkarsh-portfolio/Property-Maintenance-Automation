"use client";

import { useState } from "react";
import { Search, Plus, Mail, Phone, MapPin, MoreVertical } from "lucide-react";
import { formatDate } from "@/lib/utils";

// Demo data
const demoCustomers = [
  {
    id: 1,
    first_name: "John",
    last_name: "Smith",
    email: "john.smith@email.com",
    phone: "(555) 123-4567",
    address: "123 Main St",
    city: "Austin",
    state: "TX",
    zip_code: "78701",
    property_type: "residential",
    is_active: true,
    created_at: new Date(Date.now() - 2592000000).toISOString(),
    total_jobs: 5,
    total_spent: 2450,
  },
  {
    id: 2,
    first_name: "Sarah",
    last_name: "Johnson",
    email: "sarah.j@email.com",
    phone: "(555) 234-5678",
    address: "456 Oak Ave",
    city: "Austin",
    state: "TX",
    zip_code: "78702",
    property_type: "residential",
    is_active: true,
    created_at: new Date(Date.now() - 5184000000).toISOString(),
    total_jobs: 3,
    total_spent: 1200,
  },
  {
    id: 3,
    first_name: "Mike",
    last_name: "Davis",
    email: "mike.davis@email.com",
    phone: "(555) 345-6789",
    address: "789 Pine Rd",
    city: "Austin",
    state: "TX",
    zip_code: "78703",
    property_type: "commercial",
    is_active: true,
    created_at: new Date(Date.now() - 7776000000).toISOString(),
    total_jobs: 12,
    total_spent: 8900,
  },
  {
    id: 4,
    first_name: "Emily",
    last_name: "Brown",
    email: "emily.b@email.com",
    phone: "(555) 456-7890",
    address: "321 Elm St",
    city: "Austin",
    state: "TX",
    zip_code: "78704",
    property_type: "residential",
    is_active: true,
    created_at: new Date(Date.now() - 10368000000).toISOString(),
    total_jobs: 2,
    total_spent: 650,
  },
];

export default function CustomersPage() {
  const [customers] = useState(demoCustomers);
  const [search, setSearch] = useState("");

  const filteredCustomers = customers.filter(
    (customer) =>
      `${customer.first_name} ${customer.last_name}`
        .toLowerCase()
        .includes(search.toLowerCase()) ||
      customer.email.toLowerCase().includes(search.toLowerCase()) ||
      customer.phone.includes(search)
  );

  return (
    <div className="p-8">
      {/* Header */}
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Customers</h1>
          <p className="text-gray-500 mt-1">
            Manage your customer database
          </p>
        </div>
        <button className="btn-primary flex items-center gap-2">
          <Plus className="w-4 h-4" />
          Add Customer
        </button>
      </div>

      {/* Search */}
      <div className="relative max-w-md mb-6">
        <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
        <input
          type="text"
          placeholder="Search customers..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="input pl-10"
        />
      </div>

      {/* Customers Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {filteredCustomers.map((customer) => (
          <div key={customer.id} className="card hover:shadow-md transition-shadow">
            <div className="flex items-start justify-between mb-4">
              <div className="flex items-center gap-3">
                <div className="w-12 h-12 bg-primary-100 rounded-full flex items-center justify-center">
                  <span className="text-lg font-semibold text-primary-600">
                    {customer.first_name[0]}
                    {customer.last_name[0]}
                  </span>
                </div>
                <div>
                  <h3 className="font-semibold text-gray-900">
                    {customer.first_name} {customer.last_name}
                  </h3>
                  <span className="text-xs text-gray-500 capitalize">
                    {customer.property_type}
                  </span>
                </div>
              </div>
              <button className="p-1 hover:bg-gray-100 rounded">
                <MoreVertical className="w-4 h-4 text-gray-400" />
              </button>
            </div>

            <div className="space-y-2 mb-4">
              <div className="flex items-center gap-2 text-sm text-gray-600">
                <Mail className="w-4 h-4 text-gray-400" />
                {customer.email}
              </div>
              <div className="flex items-center gap-2 text-sm text-gray-600">
                <Phone className="w-4 h-4 text-gray-400" />
                {customer.phone}
              </div>
              <div className="flex items-center gap-2 text-sm text-gray-600">
                <MapPin className="w-4 h-4 text-gray-400" />
                {customer.address}, {customer.city}, {customer.state}
              </div>
            </div>

            <div className="flex items-center justify-between pt-4 border-t border-gray-100">
              <div className="text-center">
                <p className="text-lg font-semibold text-gray-900">
                  {customer.total_jobs}
                </p>
                <p className="text-xs text-gray-500">Jobs</p>
              </div>
              <div className="text-center">
                <p className="text-lg font-semibold text-gray-900">
                  ${customer.total_spent.toLocaleString()}
                </p>
                <p className="text-xs text-gray-500">Total Spent</p>
              </div>
              <div className="text-center">
                <p className="text-sm text-gray-600">
                  {formatDate(customer.created_at)}
                </p>
                <p className="text-xs text-gray-500">Customer Since</p>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
