"use client";

import { useState } from "react";
import {
  Search,
  Filter,
  Plus,
  Phone,
  Mail,
  Calendar,
  MoreVertical,
} from "lucide-react";
import { cn, formatDate, getStatusColor, formatCurrency } from "@/lib/utils";

// Demo data
const demoLeads = [
  {
    id: 1,
    customer: { name: "John Smith", email: "john@email.com", phone: "(555) 123-4567" },
    service_type: "hvac",
    description: "AC not cooling properly, making strange noise",
    status: "new",
    urgency: "high",
    estimated_value: 450,
    source: "website",
    created_at: new Date().toISOString(),
  },
  {
    id: 2,
    customer: { name: "Sarah Johnson", email: "sarah@email.com", phone: "(555) 234-5678" },
    service_type: "plumbing",
    description: "Leaky faucet in kitchen, water damage concern",
    status: "contacted",
    urgency: "normal",
    estimated_value: 250,
    source: "referral",
    created_at: new Date(Date.now() - 86400000).toISOString(),
  },
  {
    id: 3,
    customer: { name: "Mike Davis", email: "mike@email.com", phone: "(555) 345-6789" },
    service_type: "electrical",
    description: "Outlets sparking, circuit breaker tripping frequently",
    status: "qualified",
    urgency: "emergency",
    estimated_value: 800,
    source: "sms",
    created_at: new Date(Date.now() - 172800000).toISOString(),
  },
  {
    id: 4,
    customer: { name: "Emily Brown", email: "emily@email.com", phone: "(555) 456-7890" },
    service_type: "roofing",
    description: "Missing shingles after storm, possible leak",
    status: "estimate_sent",
    urgency: "high",
    estimated_value: 2500,
    source: "phone",
    created_at: new Date(Date.now() - 259200000).toISOString(),
  },
  {
    id: 5,
    customer: { name: "Robert Wilson", email: "robert@email.com", phone: "(555) 567-8901" },
    service_type: "pest_control",
    description: "Ant infestation in kitchen and bathroom",
    status: "won",
    urgency: "normal",
    estimated_value: 350,
    source: "website",
    created_at: new Date(Date.now() - 345600000).toISOString(),
  },
];

const statusOptions = ["all", "new", "contacted", "qualified", "estimate_sent", "won", "lost"];
const urgencyColors: Record<string, string> = {
  low: "text-gray-500",
  normal: "text-blue-500",
  high: "text-orange-500",
  emergency: "text-red-500",
};

export default function LeadsPage() {
  const [leads] = useState(demoLeads);
  const [search, setSearch] = useState("");
  const [statusFilter, setStatusFilter] = useState("all");

  const filteredLeads = leads.filter((lead) => {
    const matchesSearch =
      lead.customer.name.toLowerCase().includes(search.toLowerCase()) ||
      lead.description.toLowerCase().includes(search.toLowerCase());
    const matchesStatus = statusFilter === "all" || lead.status === statusFilter;
    return matchesSearch && matchesStatus;
  });

  return (
    <div className="p-8">
      {/* Header */}
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Leads</h1>
          <p className="text-gray-500 mt-1">
            Manage and convert your leads into customers
          </p>
        </div>
        <button className="btn-primary flex items-center gap-2">
          <Plus className="w-4 h-4" />
          Add Lead
        </button>
      </div>

      {/* Filters */}
      <div className="flex gap-4 mb-6">
        <div className="relative flex-1 max-w-md">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
          <input
            type="text"
            placeholder="Search leads..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="input pl-10"
          />
        </div>
        <div className="flex items-center gap-2">
          <Filter className="w-5 h-5 text-gray-400" />
          <select
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value)}
            className="input w-40"
          >
            {statusOptions.map((status) => (
              <option key={status} value={status}>
                {status === "all" ? "All Status" : status.replace("_", " ")}
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* Leads Table */}
      <div className="card overflow-hidden">
        <table className="w-full">
          <thead className="bg-gray-50 border-b border-gray-200">
            <tr>
              <th className="text-left px-6 py-3 text-xs font-medium text-gray-500 uppercase tracking-wider">
                Customer
              </th>
              <th className="text-left px-6 py-3 text-xs font-medium text-gray-500 uppercase tracking-wider">
                Service
              </th>
              <th className="text-left px-6 py-3 text-xs font-medium text-gray-500 uppercase tracking-wider">
                Status
              </th>
              <th className="text-left px-6 py-3 text-xs font-medium text-gray-500 uppercase tracking-wider">
                Value
              </th>
              <th className="text-left px-6 py-3 text-xs font-medium text-gray-500 uppercase tracking-wider">
                Date
              </th>
              <th className="text-left px-6 py-3 text-xs font-medium text-gray-500 uppercase tracking-wider">
                Actions
              </th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-200">
            {filteredLeads.map((lead) => (
              <tr key={lead.id} className="hover:bg-gray-50">
                <td className="px-6 py-4">
                  <div>
                    <p className="font-medium text-gray-900">
                      {lead.customer.name}
                    </p>
                    <div className="flex items-center gap-3 mt-1">
                      <span className="flex items-center gap-1 text-xs text-gray-500">
                        <Mail className="w-3 h-3" />
                        {lead.customer.email}
                      </span>
                      <span className="flex items-center gap-1 text-xs text-gray-500">
                        <Phone className="w-3 h-3" />
                        {lead.customer.phone}
                      </span>
                    </div>
                  </div>
                </td>
                <td className="px-6 py-4">
                  <div>
                    <p className="font-medium text-gray-900 capitalize">
                      {lead.service_type.replace("_", " ")}
                    </p>
                    <p className="text-sm text-gray-500 truncate max-w-xs">
                      {lead.description}
                    </p>
                    <span className={cn("text-xs font-medium", urgencyColors[lead.urgency])}>
                      {lead.urgency.toUpperCase()}
                    </span>
                  </div>
                </td>
                <td className="px-6 py-4">
                  <span className={cn("badge capitalize", getStatusColor(lead.status))}>
                    {lead.status.replace("_", " ")}
                  </span>
                </td>
                <td className="px-6 py-4">
                  <p className="font-medium text-gray-900">
                    {formatCurrency(lead.estimated_value)}
                  </p>
                  <p className="text-xs text-gray-500">{lead.source}</p>
                </td>
                <td className="px-6 py-4">
                  <div className="flex items-center gap-1 text-sm text-gray-500">
                    <Calendar className="w-4 h-4" />
                    {formatDate(lead.created_at)}
                  </div>
                </td>
                <td className="px-6 py-4">
                  <button className="p-2 hover:bg-gray-100 rounded-lg">
                    <MoreVertical className="w-4 h-4 text-gray-400" />
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
