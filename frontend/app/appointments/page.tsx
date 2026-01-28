"use client";

import { useState } from "react";
import {
  Search,
  Plus,
  Clock,
  User,
  MapPin,
  CheckCircle,
  XCircle,
  Calendar as CalendarIcon,
} from "lucide-react";
import { cn, formatDateTime, getStatusColor } from "@/lib/utils";

// Demo data
const demoAppointments = [
  {
    id: 1,
    customer: { name: "Emily Brown", address: "123 Main St, Austin, TX 78701" },
    service_type: "hvac",
    scheduled_start: new Date(Date.now() + 3600000).toISOString(),
    scheduled_end: new Date(Date.now() + 7200000).toISOString(),
    status: "confirmed",
    technician_name: "Tech Team A",
    description: "Annual AC maintenance and filter replacement",
    customer_confirmed: true,
  },
  {
    id: 2,
    customer: { name: "Robert Wilson", address: "456 Oak Ave, Austin, TX 78702" },
    service_type: "plumbing",
    scheduled_start: new Date(Date.now() + 10800000).toISOString(),
    scheduled_end: new Date(Date.now() + 14400000).toISOString(),
    status: "scheduled",
    technician_name: "Tech Team B",
    description: "Fix leaking pipe under kitchen sink",
    customer_confirmed: false,
  },
  {
    id: 3,
    customer: { name: "Lisa Anderson", address: "789 Pine Rd, Austin, TX 78703" },
    service_type: "electrical",
    scheduled_start: new Date(Date.now() + 86400000).toISOString(),
    scheduled_end: new Date(Date.now() + 90000000).toISOString(),
    status: "scheduled",
    technician_name: null,
    description: "Install new ceiling fan in living room",
    customer_confirmed: false,
  },
  {
    id: 4,
    customer: { name: "David Martinez", address: "321 Elm St, Austin, TX 78704" },
    service_type: "roofing",
    scheduled_start: new Date(Date.now() - 86400000).toISOString(),
    scheduled_end: new Date(Date.now() - 79200000).toISOString(),
    status: "completed",
    technician_name: "Tech Team C",
    description: "Roof inspection and minor repairs",
    customer_confirmed: true,
  },
];

export default function AppointmentsPage() {
  const [appointments] = useState(demoAppointments);
  const [search, setSearch] = useState("");

  const filteredAppointments = appointments.filter(
    (appt) =>
      appt.customer.name.toLowerCase().includes(search.toLowerCase()) ||
      appt.service_type.toLowerCase().includes(search.toLowerCase())
  );

  // Group appointments by date
  const today = new Date().toDateString();
  const tomorrow = new Date(Date.now() + 86400000).toDateString();

  const groupedAppointments = filteredAppointments.reduce((groups, appt) => {
    const date = new Date(appt.scheduled_start).toDateString();
    let label = date;
    if (date === today) label = "Today";
    else if (date === tomorrow) label = "Tomorrow";

    if (!groups[label]) groups[label] = [];
    groups[label].push(appt);
    return groups;
  }, {} as Record<string, typeof appointments>);

  return (
    <div className="p-8">
      {/* Header */}
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Appointments</h1>
          <p className="text-gray-500 mt-1">
            Manage scheduled service appointments
          </p>
        </div>
        <button className="btn-primary flex items-center gap-2">
          <Plus className="w-4 h-4" />
          New Appointment
        </button>
      </div>

      {/* Search */}
      <div className="relative max-w-md mb-6">
        <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
        <input
          type="text"
          placeholder="Search appointments..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="input pl-10"
        />
      </div>

      {/* Appointments List */}
      <div className="space-y-8">
        {Object.entries(groupedAppointments).map(([date, appts]) => (
          <div key={date}>
            <h2 className="text-lg font-semibold text-gray-900 mb-4 flex items-center gap-2">
              <CalendarIcon className="w-5 h-5 text-primary-600" />
              {date}
            </h2>
            <div className="space-y-4">
              {appts.map((appointment) => (
                <div
                  key={appointment.id}
                  className="card hover:shadow-md transition-shadow"
                >
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <div className="flex items-center gap-3 mb-2">
                        <h3 className="font-semibold text-gray-900">
                          {appointment.customer.name}
                        </h3>
                        <span
                          className={cn(
                            "badge capitalize",
                            getStatusColor(appointment.status)
                          )}
                        >
                          {appointment.status}
                        </span>
                        {appointment.customer_confirmed ? (
                          <span className="flex items-center gap-1 text-xs text-green-600">
                            <CheckCircle className="w-3 h-3" />
                            Confirmed
                          </span>
                        ) : (
                          <span className="flex items-center gap-1 text-xs text-orange-600">
                            <XCircle className="w-3 h-3" />
                            Pending Confirmation
                          </span>
                        )}
                      </div>

                      <p className="text-sm text-gray-600 mb-3">
                        {appointment.description}
                      </p>

                      <div className="flex flex-wrap gap-4 text-sm text-gray-500">
                        <div className="flex items-center gap-1">
                          <Clock className="w-4 h-4" />
                          {formatDateTime(appointment.scheduled_start)} -{" "}
                          {formatDateTime(appointment.scheduled_end)}
                        </div>
                        <div className="flex items-center gap-1">
                          <MapPin className="w-4 h-4" />
                          {appointment.customer.address}
                        </div>
                        {appointment.technician_name && (
                          <div className="flex items-center gap-1">
                            <User className="w-4 h-4" />
                            {appointment.technician_name}
                          </div>
                        )}
                      </div>
                    </div>

                    <div className="flex gap-2">
                      {appointment.status === "scheduled" && (
                        <>
                          <button className="btn-secondary text-sm py-1.5">
                            Reschedule
                          </button>
                          <button className="btn-primary text-sm py-1.5">
                            Confirm
                          </button>
                        </>
                      )}
                      {appointment.status === "confirmed" && (
                        <button className="btn-primary text-sm py-1.5">
                          Start Service
                        </button>
                      )}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
