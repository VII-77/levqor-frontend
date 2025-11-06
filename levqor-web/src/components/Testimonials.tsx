interface Testimonial {
  quote: string;
  author: string;
  title: string;
  company: string;
}

interface TestimonialsData {
  testimonials: Testimonial[];
}

async function getTestimonials(): Promise<TestimonialsData> {
  try {
    const res = await fetch(`${process.env.NEXT_PUBLIC_ASSETS_BASE}/marketing/testimonials.json`, {
      cache: 'no-store',
    });
    
    if (!res.ok) {
      throw new Error('Failed to fetch testimonials');
    }
    
    return res.json();
  } catch (error) {
    console.error('Error fetching testimonials:', error);
    return { testimonials: [] };
  }
}

export default async function Testimonials() {
  const data = await getTestimonials();

  if (!data.testimonials || data.testimonials.length === 0) {
    return null;
  }

  return (
    <div style={{ margin: '60px 0' }}>
      <h2 style={{
        fontSize: '32px',
        fontWeight: 700,
        textAlign: 'center',
        marginBottom: '40px',
      }}>
        What Our Customers Say
      </h2>
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))',
        gap: '24px',
      }}>
        {data.testimonials.map((testimonial, index) => (
          <div
            key={index}
            style={{
              padding: '24px',
              backgroundColor: '#f9f9f9',
              borderRadius: '8px',
              borderLeft: '4px solid #0066cc',
            }}
          >
            <p style={{
              fontSize: '16px',
              lineHeight: 1.6,
              marginBottom: '16px',
              fontStyle: 'italic',
              color: '#333',
            }}>
              "{testimonial.quote}"
            </p>
            <div>
              <p style={{ fontWeight: 600, marginBottom: '4px' }}>
                {testimonial.author}
              </p>
              <p style={{ fontSize: '14px', color: '#666' }}>
                {testimonial.title} at {testimonial.company}
              </p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
