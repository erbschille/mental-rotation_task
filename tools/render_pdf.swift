// Renders every page of a PDF to raw 8-bit grayscale pixels, using macOS's own PDF engine.
// Used by crop_items.py; you don't need to run it directly.
// usage: render_pdf <file.pdf> <outdir> <dpi>
// writes <outdir>/page<N>_<width>x<height>_<bytesPerRow>.raw (rows top to bottom)
import Foundation
import PDFKit

let args = CommandLine.arguments
guard args.count == 4, let doc = PDFDocument(url: URL(fileURLWithPath: args[1])), let dpi = Double(args[3]) else {
  FileHandle.standardError.write("usage: render_pdf <file.pdf> <outdir> <dpi>\n".data(using: .utf8)!)
  exit(1)
}
let scale = CGFloat(dpi / 72.0)
for i in 0..<doc.pageCount {
  let page = doc.page(at: i)!
  let box = page.bounds(for: .mediaBox)
  let w = Int(box.width * scale), h = Int(box.height * scale)
  let ctx = CGContext(data: nil, width: w, height: h, bitsPerComponent: 8, bytesPerRow: 0,
                      space: CGColorSpaceCreateDeviceGray(), bitmapInfo: CGImageAlphaInfo.none.rawValue)!
  ctx.setFillColor(CGColor(gray: 1, alpha: 1))
  ctx.fill(CGRect(x: 0, y: 0, width: w, height: h))
  ctx.scaleBy(x: scale, y: scale)
  page.draw(with: .mediaBox, to: ctx)
  let data = Data(bytes: ctx.data!, count: ctx.bytesPerRow * h)
  try! data.write(to: URL(fileURLWithPath: "\(args[2])/page\(i + 1)_\(w)x\(h)_\(ctx.bytesPerRow).raw"))
}
print(doc.pageCount)
