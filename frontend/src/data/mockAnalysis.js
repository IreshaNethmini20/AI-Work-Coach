/**
 * Mock analysis data for development
 * This will be replaced with API responses when backend is implemented
 */

export const analysisResult = {
  task: "Prepare a weekly sales report for my manager",
  aiOpportunity: {
    level: "HIGH",
    message: "AI can significantly assist with this task while keeping human review for the final report."
  },
  recommendedWorkflow: [
    {
      step: 1,
      title: "Collect and prepare the sales data",
      description: "Gather relevant sales metrics and organize data for analysis"
    },
    {
      step: 2,
      title: "Use AI to identify important trends",
      description: "Let AI analyze patterns, anomalies, and key insights in the data"
    },
    {
      step: 3,
      title: "Generate a concise management summary",
      description: "Create executive summary highlighting key findings"
    },
    {
      step: 4,
      title: "Review AI-generated insights",
      description: "Validate AI suggestions against business context"
    },
    {
      step: 5,
      title: "Prepare the final report",
      description: "Combine human expertise with AI insights for the final deliverable"
    }
  ],
  skillToPractice: {
    name: "AI-assisted data analysis",
    category: "Data Skills",
    level: "Intermediate"
  },
  readyToUsePrompt: "Analyse the following weekly sales data and identify the most important trends, changes, anomalies, and business insights. Present the findings clearly for a management audience.",
  expectedBenefit: "Reduce repetitive reporting work while keeping human review for important business decisions.",
  humanReview: "AI-generated analysis should be reviewed before being used in a business report."
};
