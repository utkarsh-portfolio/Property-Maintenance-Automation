import Link from "next/link";
import { ArrowRight, Clock, User } from "lucide-react";
import { cn, formatDateTime, getStatusColor } from "@/lib/utils";

interface Appointment {
  id: number;
  customer_name: string;
  service_type: string;
  scheduled_start: string;
  status: string;
  technician_name: string | null;
}

export default function TodayAppointments({
  appointments,
}: {
  appointments: Appointment[];
}) {
  return (
    <div className="card">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-lg font-semibold text-gray-900">
          Today&apos;s Appointments
        </h2>
        <Link
          href="/appointments"
          className="text-sm text-primary-600 hover:text-primary-700 flex items-center gap-1"
        >
          View all <ArrowRight className="w-4 h-4" />
        </Link>
      </div>

      {appointments.length === 0 ? (
        <div className="text-center py-8 text-gray-500">
          <Calendar className="w-12 h-12 mx-auto mb-3 text-gray-300" />
          <p>No appointments scheduled for today</p>
        </div>
      ) : (
        <div className="space-y-4">
          {appointments.map((appointment) => (
            <div
              key={appointment.id}
              className="flex items-center gap-4 p-4 rounded-lg border border-gray-100 hover:border-primary-200 transition-colors"
            >
              <div className="flex-1">
                <div className="flex items-center gap-2 mb-1">
                  <p className="font-medium text-gray-900">
                    {appointment.customer_name}
                  </p>
                  <span
                    className={cn(
                      "badge capitalize",
                      getStatusColor(appointment.status)
                    )}
                  >
                    {appointment.status}
                  </span>
                </div>
                <p className="text-sm text-gray-500 capitalize">
                  {appointment.service_type.replace("_", " ")}
                </p>
              </div>
              <div className="text-right">
                <div className="flex items-center gap-1 text-sm text-gray-600">
                  <Clock className="w-4 h-4" />
                  {formatDateTime(appointment.scheduled_start)}
                </div>
                {appointment.technician_name && (
                  <div className="flex items-center gap-1 text-sm text-gray-500 mt-1">
                    <User className="w-4 h-4" />
                    {appointment.technician_name}
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

// Import Calendar icon for empty state
import { Calendar } from "lucide-react";
