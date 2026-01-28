"use client";

import { useState } from "react";
import {
  Bell,
  MessageSquare,
  CreditCard,
  Shield,
  Palette,
  Save,
} from "lucide-react";

export default function SettingsPage() {
  const [settings, setSettings] = useState({
    notifications: {
      email: true,
      sms: true,
      push: false,
    },
    ai: {
      autoRespond: true,
      leadCapture: true,
      followUpReminders: true,
    },
    business: {
      companyName: "PropertyPro Maintenance",
      phone: "(555) 000-0000",
      email: "contact@propertypro.com",
      address: "100 Business Ave, Austin, TX 78701",
    },
  });

  return (
    <div className="p-8 max-w-4xl">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-gray-900">Settings</h1>
        <p className="text-gray-500 mt-1">
          Manage your application preferences
        </p>
      </div>

      {/* Settings Sections */}
      <div className="space-y-8">
        {/* Business Info */}
        <section className="card">
          <h2 className="text-lg font-semibold text-gray-900 mb-4 flex items-center gap-2">
            <CreditCard className="w-5 h-5 text-primary-600" />
            Business Information
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Company Name
              </label>
              <input
                type="text"
                value={settings.business.companyName}
                onChange={(e) =>
                  setSettings({
                    ...settings,
                    business: { ...settings.business, companyName: e.target.value },
                  })
                }
                className="input"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Phone
              </label>
              <input
                type="text"
                value={settings.business.phone}
                onChange={(e) =>
                  setSettings({
                    ...settings,
                    business: { ...settings.business, phone: e.target.value },
                  })
                }
                className="input"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Email
              </label>
              <input
                type="email"
                value={settings.business.email}
                onChange={(e) =>
                  setSettings({
                    ...settings,
                    business: { ...settings.business, email: e.target.value },
                  })
                }
                className="input"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Address
              </label>
              <input
                type="text"
                value={settings.business.address}
                onChange={(e) =>
                  setSettings({
                    ...settings,
                    business: { ...settings.business, address: e.target.value },
                  })
                }
                className="input"
              />
            </div>
          </div>
        </section>

        {/* Notifications */}
        <section className="card">
          <h2 className="text-lg font-semibold text-gray-900 mb-4 flex items-center gap-2">
            <Bell className="w-5 h-5 text-primary-600" />
            Notifications
          </h2>
          <div className="space-y-4">
            {[
              { key: "email", label: "Email Notifications", desc: "Receive updates via email" },
              { key: "sms", label: "SMS Notifications", desc: "Get text message alerts" },
              { key: "push", label: "Push Notifications", desc: "Browser push notifications" },
            ].map((item) => (
              <div key={item.key} className="flex items-center justify-between">
                <div>
                  <p className="font-medium text-gray-900">{item.label}</p>
                  <p className="text-sm text-gray-500">{item.desc}</p>
                </div>
                <label className="relative inline-flex items-center cursor-pointer">
                  <input
                    type="checkbox"
                    checked={settings.notifications[item.key as keyof typeof settings.notifications]}
                    onChange={(e) =>
                      setSettings({
                        ...settings,
                        notifications: {
                          ...settings.notifications,
                          [item.key]: e.target.checked,
                        },
                      })
                    }
                    className="sr-only peer"
                  />
                  <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-primary-100 rounded-full peer peer-checked:after:translate-x-full rtl:peer-checked:after:-translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:start-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-primary-600"></div>
                </label>
              </div>
            ))}
          </div>
        </section>

        {/* AI Settings */}
        <section className="card">
          <h2 className="text-lg font-semibold text-gray-900 mb-4 flex items-center gap-2">
            <MessageSquare className="w-5 h-5 text-primary-600" />
            AI Agent Settings
          </h2>
          <div className="space-y-4">
            {[
              { key: "autoRespond", label: "Auto-Respond to Messages", desc: "AI automatically handles incoming messages" },
              { key: "leadCapture", label: "Automatic Lead Capture", desc: "Create leads from conversations" },
              { key: "followUpReminders", label: "Follow-up Reminders", desc: "AI sends follow-up reminders for estimates" },
            ].map((item) => (
              <div key={item.key} className="flex items-center justify-between">
                <div>
                  <p className="font-medium text-gray-900">{item.label}</p>
                  <p className="text-sm text-gray-500">{item.desc}</p>
                </div>
                <label className="relative inline-flex items-center cursor-pointer">
                  <input
                    type="checkbox"
                    checked={settings.ai[item.key as keyof typeof settings.ai]}
                    onChange={(e) =>
                      setSettings({
                        ...settings,
                        ai: {
                          ...settings.ai,
                          [item.key]: e.target.checked,
                        },
                      })
                    }
                    className="sr-only peer"
                  />
                  <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-primary-100 rounded-full peer peer-checked:after:translate-x-full rtl:peer-checked:after:-translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:start-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-primary-600"></div>
                </label>
              </div>
            ))}
          </div>
        </section>

        {/* API Keys Info */}
        <section className="card bg-gray-50">
          <h2 className="text-lg font-semibold text-gray-900 mb-4 flex items-center gap-2">
            <Shield className="w-5 h-5 text-primary-600" />
            API Configuration
          </h2>
          <p className="text-sm text-gray-600 mb-4">
            Configure your API keys in the backend <code className="bg-gray-200 px-1 rounded">.env</code> file:
          </p>
          <div className="bg-gray-900 text-gray-100 rounded-lg p-4 text-sm font-mono overflow-x-auto">
            <pre>{`# Groq AI (Free)
GROQ_API_KEY=your_groq_key

# Twilio (Free trial)
TWILIO_ACCOUNT_SID=your_sid
TWILIO_AUTH_TOKEN=your_token
TWILIO_PHONE_NUMBER=+1234567890

# Database (Neon - Free)
DATABASE_URL=postgresql+asyncpg://...`}</pre>
          </div>
        </section>

        {/* Save Button */}
        <div className="flex justify-end">
          <button className="btn-primary flex items-center gap-2">
            <Save className="w-4 h-4" />
            Save Changes
          </button>
        </div>
      </div>
    </div>
  );
}
