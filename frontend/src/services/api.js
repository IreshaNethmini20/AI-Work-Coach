const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '';

async function request(path, payload) {
  let response;

  try {
    response = await fetch(`${API_BASE_URL}${path}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(payload),
    });
  } catch {
    throw new Error('The AI Work Coach API is unavailable.');
  }

  if (!response.ok) {
    throw new Error('The AI Work Coach API could not complete this request.');
  }

  return response.json();
}

export function analyzeTask(taskDescription) {
  return request('/api/analyze', { task: taskDescription });
}

export function submitFeedback(feedback) {
  return request('/api/feedback', feedback);
}