export async function prepareImage(file?: File): Promise<string> {
  if (!file) throw new Error('اختر صورة السيارة أولًا.');
  if (!['image/jpeg','image/png','image/webp','image/avif','image/gif'].includes(file.type))
    throw new Error('اختر صورة بصيغة JPG أو PNG أو WebP أو AVIF أو GIF.');
  if (file.size > 12 * 1024 * 1024) throw new Error('حجم الصورة أكبر من 12 ميجابايت. اختر صورة أصغر.');
  const url = URL.createObjectURL(file);
  try {
    const image = new Image();
    image.src = url;
    await image.decode();
    if (!image.naturalWidth || !image.naturalHeight) throw new Error();
    return url;
  } catch {
    URL.revokeObjectURL(url);
    throw new Error('تعذّر فتح الصورة. جرّب صورة أخرى.');
  }
}
