import React, { useEffect, useState } from "react";

interface RecommendationResponse {
  userRole: string;
  userId: string;
  businessId: string;
  recommendationType: string;
  companyData: string;
}

const Recommendations: React.FC = () => {
  const [data, setData] = useState<RecommendationResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      try {
        const payload = {
          userRole: "Admin",
          userId: "66b6b257d802e08b54bee8f5",
          businessId: "66b6b16eeb02b55711d8052c",
          recommendationType: "brandCultureStrategy",
          companyData:
            "{\\\"info\\\":{\\\"employeeFocusPriority\\\":\\\"High\\\",\\\"focus\\\":[\\\"Sales & Marketing\\\"],\\\"background\\\":\\\"Development\\\",\\\"challenges\\\":\\\"Development\\\",\\\"leadershipRoles\\\":[\\\"Chief Human Resource Officer (CHRO)\\\",\\\"Chief Product Officer (CPO)\\\",\\\"Chief Data Officer (CDO)\\\",\\\"Chief Marketing Officer (CMO)\\\",\\\"Senior Leaders in Organizational Development\\\",\\\"Other Leaders\\\"],\\\"HRIS\\\":\\\"Development\\\",\\\"PMS\\\":\\\"Development\\\",\\\"neededIntegrations\\\":\\\"Development\\\",\\\"desiredModules\\\":[],\\\"onboardingETA\\\":\\\"0 Days\\\",\\\"neededCofiguration\\\":\\\"Development\\\",\\\"dataPrivacyRequirement\\\":\\\"Development\\\",\\\"securityComplainceStandard\\\":[\\\"General Data Protection Regulation (GDPR)\\\",\\\"Health Insurance Portablity and Accountability Act (HIPAA)\\\"],\\\"otherComplianceNeeded\\\":\\\"Development\\\",\\\"annualRevenue\\\":50000000,\\\"employeeCount\\\":100,\\\"businessStartYear\\\":2021},\\\"name\\\":\\\"Culturefy Development\\\",\\\"notes\\\":\\\"Development\\\",\\\"size\\\":\\\"1000+\\\"}"
        };

        const res = await fetch("https://robifastculturefy.azurewebsites.net/api/v1/recommendation/recommendations", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(payload),
        });
        if (!res.ok) throw new Error("Failed to fetch data");
        const json = await res.json();
        setData(json);
      } catch (err: any) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) return <div className="p-4 text-lg">Loading...</div>;
  if (error) return <div className="p-4 text-red-500">Error: {error}</div>;

  const parsedCompanyData = data ? JSON.parse(data.companyData) : null;

  return (
    <div className="p-6 max-w-3xl mx-auto space-y-4">
      <h1 className="text-2xl font-bold">Recommendation Output</h1>
      {data && (
        <div className="space-y-2 bg-white shadow rounded-xl p-4">
          <p><strong>User Role:</strong> {data.userRole}</p>
          <p><strong>User ID:</strong> {data.userId}</p>
          <p><strong>Business ID:</strong> {data.businessId}</p>
          <p><strong>Recommendation Type:</strong> {data.recommendationType}</p>

          {parsedCompanyData && (
            <div className="mt-4 p-4 border rounded-xl bg-gray-50">
              <h2 className="text-xl font-semibold mb-2">Company Data</h2>
              <pre className="whitespace-pre-wrap text-sm">{JSON.stringify(parsedCompanyData, null, 2)}</pre>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default Recommendations;
