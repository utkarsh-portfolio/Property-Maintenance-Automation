"use client";

import { useState, useEffect } from "react";
import {
  BarChart3,
  TrendingUp,
  Users,
  Calendar,
  MessageSquare,
  DollarSign,
  ArrowUp,
  ArrowDown,
  RefreshCw,
} from "lucide-react";
import { api } from "@/lib/api";

interface DashboardStats {
  leads: {
    total: number;
    this_week: number;
    conversion_rate: number;
  };
  appointments: {
    today: number;
  };
  customers: {
    total: number;
  };
  conversations: {
    active: number;
    ai_messages_week: number;
  };
  revenue: {
    this_month: number;
  };
}

interface ChartData {
  date: string;
  count?: number;
  revenue?: number;
}

export default function AnalyticsPage() {
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [leadsTrend, setLeadsTrend] = useState<ChartData[]>([]);
  const [leadsByStatus, setLeadsByStatus] = useState<Record<string, number>>({});
  const [leadsByService, setLeadsByService] = useState<{ service: string; count: number }[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchAnalytics();
  }, []);

  const fetchAnalytics = async () => {
    setLoading(true);
    try {
      const [dashboardRes, trendRes, statusRes, serviceRes] = await Promise.all([
        api.get("/analytics/dashboard"),
        api.get("/analytics/leads/trend?days=30"),
        api.get("/analytics/leads/by-status"),
        api.get("/analytics/leads/by-service"),
      ]);

      setStats(dashboardRes.data);
      setLeadsTrend(trendRes.data.data);
      setLeadsByStatus(statusRes.data.data);
      setLeadsByService(serviceRes.data.data);
    } catch (error) {
      console.error("Failed to fetch analytics:", error);
    } finally {
      setLoading(false);
    }
  };

  const statusColors: Record<string, string> = {
    new: "bg-blue-500",
    contacted: "bg-yellow-500",
    qualified: "bg-purple-500",
    estimate_sent: "bg-orange-500",
    converted: "bg-green-500",
    lost: "bg-red-500",
  };

  const maxLeadCount = Math.max(...leadsTrend.map((d) => d.count || 0), 1);
  const totalLeadsByStatus = Object.values(leadsByStatus).reduce((a, b) => a + b, 0) || 1;

  if (loading) {
    return (
      <div className="p-8 flex items-center justify-center min-h-screen">
        <RefreshCw className="w-8 h-8 animate-spin text-primary-600" />
      </div>
    );
  }

  return (
    <div className="p-8">
      {/* Header */}
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Analytics</h1>
          <p className="text-gray-500 mt-1">Track performance and insights</p>
        </div>
        <button
          onClick={fetchAnalytics}
          className="btn-secondary flex items-center gap-2"
        >
          <RefreshCw className="w-4 h-4" />
          Refresh
        </button>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <StatCard
          title="Total Leads"
          value={stats?.leads.total || 0}
          change={stats?.leads.this_week || 0}
          changeLabel="this week"
          icon={<TrendingUp className="w-5 h-5" />}
          color="blue"
        />
        <StatCard
          title="Conversion Rate"
          value={`${stats?.leads.conversion_rate || 0}%`}
          icon={<BarChart3 className="w-5 h-5" />}
          color="green"
        />
        <StatCard
          title="AI Messages"
          value={stats?.conversations.ai_messages_week || 0}
          changeLabel="this week"
          icon={<MessageSquare className="w-5 h-5" />}
          color="purple"
        />
        <StatCard
          title="Monthly Revenue"
          value={`$${(stats?.revenue.this_month || 0).toLocaleString()}`}
          icon={<DollarSign className="w-5 h-5" />}
          color="emerald"
        />
      </div>

      {/* Charts Row */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        {/* Leads Trend Chart */}
        <div className="card">
          <h3 className="font-semibold text-gray-900 mb-4">Leads Trend (30 Days)</h3>
          <div className="h-48 flex items-end gap-1">
            {leadsTrend.length > 0 ? (
              leadsTrend.map((day, index) => (
                <div
                  key={index}
                  className="flex-1 bg-primary-500 rounded-t hover:bg-primary-600 transition-colors cursor-pointer group relative"
                  style={{
                    height: `${((day.count || 0) / maxLeadCount) * 100}%`,
                    minHeight: day.count ? "4px" : "0",
                  }}
                >
                  <div className="absolute bottom-full left-1/2 -translate-x-1/2 mb-2 px-2 py-1 bg-gray-900 text-white text-xs rounded opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap">
                    {day.date}: {day.count} leads
                  </div>
                </div>
              ))
            ) : (
              <div className="w-full h-full flex items-center justify-center text-gray-400">
                No data available
              </div>
            )}
          </div>
          <div className="flex justify-between mt-2 text-xs text-gray-500">
            <span>30 days ago</span>
            <span>Today</span>
          </div>
        </div>

        {/* Leads by Status */}
        <div className="card">
          <h3 className="font-semibold text-gray-900 mb-4">Leads by Status</h3>
          <div className="space-y-3">
            {Object.entries(leadsByStatus).map(([status, count]) => (
              <div key={status}>
                <div className="flex justify-between text-sm mb-1">
                  <span className="capitalize text-gray-600">
                    {status.replace("_", " ")}
                  </span>
                  <span className="font-medium">{count}</span>
                </div>
                <div className="h-2 bg-gray-100 rounded-full overflow-hidden">
                  <div
                    className={`h-full ${statusColors[status] || "bg-gray-400"} rounded-full transition-all`}
                    style={{ width: `${(count / totalLeadsByStatus) * 100}%` }}
                  />
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Service Breakdown */}
      <div className="card">
        <h3 className="font-semibold text-gray-900 mb-4">Leads by Service Type</h3>
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
          {leadsByService.map((item) => (
            <div
              key={item.service}
              className="p-4 bg-gray-50 rounded-lg text-center hover:bg-gray-100 transition-colors"
            >
              <p className="text-2xl font-bold text-primary-600">{item.count}</p>
              <p className="text-sm text-gray-600 capitalize mt-1">
                {item.service.replace("_", " ")}
              </p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

function StatCard({
  title,
  value,
  change,
  changeLabel,
  icon,
  color,
}: {
  title: string;
  value: string | number;
  change?: number;
  changeLabel?: string;
  icon: React.ReactNode;
  color: "blue" | "green" | "purple" | "emerald";
}) {
  const colorClasses = {
    blue: "bg-blue-50 text-blue-600",
    green: "bg-green-50 text-green-600",
    purple: "bg-purple-50 text-purple-600",
    emerald: "bg-emerald-50 text-emerald-600",
  };

  return (
    <div className="card">
      <div className="flex items-center justify-between mb-3">
        <span className="text-sm text-gray-500">{title}</span>
        <div className={`p-2 rounded-lg ${colorClasses[color]}`}>{icon}</div>
      </div>
      <p className="text-2xl font-bold text-gray-900">{value}</p>
      {change !== undefined && (
        <div className="flex items-center gap-1 mt-2">
          {change > 0 ? (
            <ArrowUp className="w-4 h-4 text-green-500" />
          ) : (
            <ArrowDown className="w-4 h-4 text-red-500" />
          )}
          <span className="text-sm text-gray-600">
            +{change} {changeLabel}
          </span>
        </div>
      )}
    </div>
  );
}
