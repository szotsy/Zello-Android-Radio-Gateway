const MAX_UPLOAD_BYTES = 10 * 1024 * 1024;
function response(body, status = 200, extra = {}) {
  return new Response(JSON.stringify(body), { status, headers: {
    "Content-Type": "application/json; charset=utf-8", "Cache-Control": "no-store",
    "Access-Control-Allow-Origin": "*", "Access-Control-Allow-Methods": "POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type, X-OG-App-Version, X-OG-Session",
    "Access-Control-Max-Age": "86400", "Vary": "Origin", ...extra
  }});
}
export default {
  async fetch(request, env) {
    if (request.method === "OPTIONS") return new Response(null, {status:204, headers: response({}).headers});
    const url = new URL(request.url);
    if (url.pathname !== "/api/diagnostics" || request.method !== "POST") return response({ok:false,error:"Not found"},404);
    const ip = request.headers.get("CF-Connecting-IP") || "unknown";
    if (env.UPLOAD_LIMIT) {
      const result = await env.UPLOAD_LIMIT.limit({key:ip});
      if (!result.success) return response({ok:false,error:"Too many uploads. Try again later."},429);
    }
    const length = Number(request.headers.get("Content-Length") || "0");
    if (length > MAX_UPLOAD_BYTES) return response({ok:false,error:"Maximum ZIP size is 10 MB."},413);
    const type = (request.headers.get("Content-Type") || "").toLowerCase();
    if (!type.includes("zip") && !type.includes("octet-stream")) return response({ok:false,error:"Send the diagnostic ZIP as application/zip."},415);
    const body = await request.arrayBuffer();
    if (body.byteLength < 4 || body.byteLength > MAX_UPLOAD_BYTES) return response({ok:false,error:"Invalid ZIP size."},413);
    const b = new Uint8Array(body);
    const valid = b[0]===0x50 && b[1]===0x4b && ((b[2]===0x03&&b[3]===0x04)||(b[2]===0x05&&b[3]===0x06)||(b[2]===0x07&&b[3]===0x08));
    if (!valid) return response({ok:false,error:"The uploaded file is not a ZIP archive."},400);
    const id = crypto.randomUUID();
    const appVersion = (request.headers.get("X-OG-App-Version") || "unknown").slice(0,40);
    const session = (request.headers.get("X-OG-Session") || "").replace(/[^a-zA-Z0-9_-]/g,"").slice(0,64);
    const date = new Date().toISOString().slice(0,10);
    const key = "incoming/" + date + "/" + id + ".zip";
    await env.DIAGNOSTIC_LOGS.put(key, body, {httpMetadata:{contentType:"application/zip",cacheControl:"private, no-store"},customMetadata:{uploadId:id,appVersion,session,receivedAt:new Date().toISOString()}});
    return response({ok:true,uploadId:id,message:"Diagnostic log received. Thank you."},201);
  }
};
