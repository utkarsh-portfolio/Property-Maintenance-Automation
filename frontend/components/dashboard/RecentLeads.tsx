import Link from "next/link";
import { ArrowRight, Thermometer, Droplet, Zap, Home, Bug, Wrench } from "lucide-react";
import { cn, getStatusColor } from "@/lib/utils";

interface Lead {
  id: number;
  customer_name: string;
  service_type: string;
  status: string;
  urgency: string;
  created_at: string;
}

const serviceIcons: Record<string, React.ComponentType<{ className?: string }>> = {
  hvac: Thermometer,
  plumbing: Droplet,
  electrical: Zap,
  roofing: Home,
  pest_control: Bug,
  general_maintenance: Wrench,
};

const urgencyColors: Record<string, string> = {
  low: "bg-gray-100 text-gray-600",
  normal: "bg-blue-100 text-blue-600",
  high: "bg-orange-100 text-orange-600",
  emergency: "bg-red-100 text-red-600",
};

export default function RecentLeads({ leads }: { leads: Lead[] }) {
  return (
    <div className="card">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-lg font-semibold text-gray-900">Recent Leads</h2>
        <Link
          href="/leads"
          className="text-sm text-primary-600 hover:text-primary-700 flex items-center gap-1"
        >
          View all <ArrowRight className="w-4 h-4" />
        </Link>
      </div>

      <div className="space-y-4">
        {leads.map((lead) => {
          const ServiceIcon = serviceIcons[lead.service_type] || Wrench;
          return (
            <div
              key={lead.id}
              className="flex items-center gap-4 p-3 rounded-lg hover:bg-gray-50 transition-colors"
            >
              <div className="bg-primary-50 p-2 rounded-lg">
                <ServiceIcon className="w-5 h-5 text-primary-600" />
              </div>
              <div className="flex-1 min-w-0">
                <p className="font-medium text-gray-900 truncate">
                  {lead.customer_name}
                </p>
                <p className="text-sm text-gray-500 capitalize">
                  {lead.service_type.replace("_", " ")}
                </p>
              </div>
              <div className="flex items-center gap-2">
                <span
                  className={cn(
                    "badge capitalize",
                    urgencyColors[lead.urgency]
                  )}
                >
                  {lead.urgency}
                </span>
                <span className={cn("badge capitalize", getStatusColor(lead.status))}>
                  {lead.status}
                </span>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
