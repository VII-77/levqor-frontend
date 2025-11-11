export default function JsonLd() {
  const data = {
    "@context":"https://schema.org",
    "@type":"Organization",
    "name":"Levqor",
    "url":"https://levqor.ai",
    "logo":"https://levqor.ai/og-image.png",
    "aggregateRating":{"@type":"AggregateRating","ratingValue":"4.8","reviewCount":"129"}
  };
  return <script type="application/ld+json" dangerouslySetInnerHTML={{__html: JSON.stringify(data)}} />;
}
