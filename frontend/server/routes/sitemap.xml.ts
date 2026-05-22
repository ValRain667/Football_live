export default defineEventHandler(() => {
  const urls = [
    '', '/matches', '/live', '/leagues', '/teams', '/standings/39', '/news', '/login', '/register',
  ];
  const xml = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${urls.map(u => `  <url><loc>https://footballlivehub.com${u}</loc></url>`).join('\n')}
</urlset>`;
  return xml;
});
