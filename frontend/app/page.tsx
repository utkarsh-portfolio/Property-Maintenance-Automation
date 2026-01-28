"use client";

import { useEffect, useState } from "react";
import {
  Target,
  Calendar,
  DollarSign,
  TrendingUp,
  Clock,
  CheckCircle,
  AlertCircle,
  Users,
} from "lucide-react";
import { formatCurrency, getStatusColor } from "@/lib/utils";
import StatsCard from "@/components/dashboard/StatsCard";
import RecentLeads from "@/components/dashboard/RecentLeads";
import TodayAppointments from "@/components/dashboard/TodayAppointments";

// Demo data for the dashboard
const demoStats = {
  total_leads: 156,
  new_leads: 23,
  qualified_leads: 45,
  won_leads: 67,
  lost_leads: 21,
  conversion_rate: 76.1,
  total_value: 245680,
};

const demoLeads = [
  {
    id: 1,
    customer_name: "John Smith",
    service_type: "hvac",
    status: "new",
    urgency: "high",
    created_at: new Date().toISOString(),
  },
  {
    id: 2,
    customer_name: "Sarah Johnson",
    service_type: "plumbing",
    status: "contacted",
    urgency: "normal",
    created_at: new Date(Date.now() - 3600000).toISOString(),
  },
  {
    id: 3,
    customer_name: "Mike Davis",
    service_type: "electrical",
    status: "qualified",
    urgency: "emergency",
    created_at: new Date(Date.now() - 7200000).toISOString(),
  },
];

const demoAppointments = [
  {
    id: 1,
    customer_name: "Emily Brown",
    service_type: "hvac",
    scheduled_start: new Date(Date.now() + 3600000).toISOString(),
    status: "confirmed",
    technician_name: "Tech Team A",
  },
  {
    id: 2,
    customer_name: "Robert Wilson",
    service_type: "plumbing",
    scheduled_start: new Date(Date.now() + 7200000).toISOString(),
    status: "scheduled",
    technician_name: "Tech Team B",
  },
];

export default function Dashboard() {
  const [stats, setStats] = useState(demoStats);
  const [leads, setLeads] = useState(demoLeads);
  const [appointments, setAppointments] = useState(demoAppointments);

  return (
    <div className="p-8">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
        <p className="text-gray-500 mt-1">
          Overview of your property maintenance operations
        </p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <StatsCard
          title="Total Leads"
          value={stats.total_leads}
          icon={Target}
          trend="+12%"
          trendUp={true}
        />
        <StatsCard
          title="New Leads"
          value={stats.new_leads}
          icon={AlertCircle}
          subtitle="Awaiting contact"
          color="blue"
        />
        <StatsCard
          title="Conversion Rate"
          value={`${stats.conversion_rate}%`}
          icon={TrendingUp}
          trend="+5.2%"
          trendUp={true}
          color="green"
        />
        <StatsCard
          title="Revenue"
          value={formatCurrency(stats.total_value)}
          icon={DollarSign}
          trend="+18%"
          trendUp={true}
          color="purple"
        />
      </div>

      {/* Content Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Recent Leads */}
        <RecentLeads leads={leads} />

        {/* Today's Appointments */}
        <TodayAppointments appointments={appointments} />
      </div>

      {/* AI Agent Status */}
      <div className="mt-8 card">
        <div className="flex items-center justify-between">
          <div>
            <h3 className="font-semibold text-gray-900">AI Agent Activity</h3>
            <p className="text-sm text-gray-500 mt-1">
              Automated conversations and lead handling
            </p>
          </div>
          <div className="flex items-center gap-4">
            <div className="text-center">
              <p className="text-2xl font-bold text-primary-600">47</p>
              <p className="text-xs text-gray-500">Conversations Today</p>
            </div>
            <div className="text-center">
              <p className="text-2xl font-bold text-green-600">12</p>
              <p className="text-xs text-gray-500">Leads Generated</p>
            </div>
            <div className="text-center">
              <p className="text-2xl font-bold text-purple-600">8</p>
              <p className="text-xs text-gray-500">Appointments Booked</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
