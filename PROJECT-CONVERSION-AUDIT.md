# Audit cấu trúc và quy trình chuyển index.html → index2.html

Ngày kiểm tra: 09/11/2026. Checkout: 6829153. Phạm vi: mã nguồn, bộ sinh, tài nguyên, tài liệu và bằng chứng trong reference. Không sửa giao diện hoặc chạy lại browser/Lighthouse trong lượt này. Số đo thị giác bên dưới thuộc snapshot được lưu, không phải phép đo live mới.

## Kết luận

index.html là bản tái hiện thiết kế bằng SVG và tọa độ. index2.html là bản HTML có ngữ nghĩa, được sinh từ dữ liệu trích xuất của bản SVG. Bản hiện tại giữ nội dung nhưng chưa hoàn thành chuyển đổi trung thành về thị giác cho toàn trang. Header có template và CSS chuyên biệt; phần lớn section 02–21 dùng một renderer và hệ lưới chung. Không thể dùng báo cáo nghiệm thu cũ để xác nhận bản này giống nguồn.

## Bản đồ dự án

| Nhóm | Vai trò |
|---|---|
| index.html, fidelity.css, fidelity.js | Trang chuẩn, khung 22 section, lazy-load script SVG |
| assets/faithful/01.js…22.js, section.js, section.css | Artwork và cơ chế dựng SVG/reflow mobile |
| assets/faithful/media, fonts, fonts.css | Ảnh và font nguồn |
| build-fidelity.py, assets/figma | Tuyến nhập dữ liệu thiết kế Figma; không phải bộ sinh HTML mới |
| build-index2.py | Bộ sinh index2.html từ fixture và manifest ảnh |
| index2.css | Style thẻ, danh sách sản phẩm, carousel, footer và responsive dùng chung |
| index2-header.css | Font bổ sung, hình học và responsive riêng section 01 |
| index2.js | Menu, thông báo demo, yêu thích, bộ đếm giỏ hàng, carousel, form |
| assets/index2 | Asset WebP, ảnh sản phẩm, artwork đã xử lý |
| tools/index2 | Trích xuất, chuẩn bị ảnh, kiểm tra và báo cáo qua nhiều thế hệ |
| app.js, refine.js, styles.css, reference/previous-index.html | Tuyến triển khai trước; không được index.html/index2.html hiện tại nạp trực tiếp |

## Cách chuyển đổi thực tế

1. index.html cung cấp vị trí và kích thước 22 section trên frame 1920 × 20142. fidelity.js quan sát viewport rồi nạp assets/faithful/NN.js. HacomArt.register đưa SVG vào section và gọi cơ chế mount/reflow.
2. tools/index2/capture-index2.js trích nội dung, bounding box, computed style, text, card, action và artwork; phần artwork được clone rồi bỏ text/foreignObject. Fixture desktop và mobile giữ kết quả để bộ sinh không cần chạy trình duyệt khi build.
3. reference/index2-desktop-source.json là nội dung desktop; index2-mobile-source.json chứa các piece để phân nhóm nội dung. Đây là đầu vào build, không chỉ là bằng chứng kiểm thử.
4. tools/index2/content-images.json ánh xạ ảnh nguồn sang WebP và kích thước. product-photos.json ánh xạ ảnh của 30 sản phẩm. source_images() lần theo tham chiếu SVG có thể đi tới và loại trừ một số artwork UI để tránh dùng lại cả cụm giao diện.
5. render_header() dựng riêng thanh thông tin, tìm kiếm, account, danh mục, quick nav, hero, banner và cam kết. render_section() gom sản phẩm theo trường card, gom phần còn lại theo mobile pieces và dựng content-card. render_footer() dựng newsletter, địa điểm và thông tin liên hệ.
6. python build-index2.py xuất HTML hoàn chỉnh. CSS và JS sửa trực tiếp. Tuyến hiện tại không gọi normalize-header.py, không sinh token chữ cũ và không giữ hình học từng section thân trang bằng tọa độ nguồn.
7. So sánh cần đồng thời kiểm tra chữ, hình học, baseline, font, crop, path icon, responsive và tương tác. Chỉ khớp text hoặc chiều cao không đủ nghiệm thu.

## Phân loại reference

Thư mục hiện có 429 file, tổng 242421989 byte, khoảng 231 MiB.

| Nhóm | Cách sử dụng |
|---|---|
| index2-desktop-source.json, index2-mobile-source.json | Đầu vào trực tiếp của bộ sinh; không xóa hoặc thay bằng snapshot mới tùy ý |
| section-1-visual-guide.md và section-1-audit/ | Hướng dẫn hiệu chỉnh header gần tuyến mã hiện tại nhất: source/current/overlay/diff, JSON hình học, CSV baseline, responsive và smoke test chặn ảnh |
| desktop-1920/, fidelity-*.json, figma-section-bounds.json | Đối chiếu bản SVG với thiết kế và hành vi nguồn |
| index2-visual/, header-native-visual/ | Bằng chứng qua các phiên bản chuyển đổi trước; phải đối chiếu phiên bản trước khi dùng |
| *-commands.json, *-results.json | Lệnh kiểm thử lưu sẵn và kết quả tương ứng; không mặc định phản ánh HEAD |
| index2-lighthouse/, header-native-lighthouse/ | Báo cáo lab cũ; không dùng điểm làm kết quả hiện tại |
| previous-index.html, verification.json ở root | Bằng chứng tuyến demo trước; giới hạn nội dung 1800px trong verification không phải chuẩn 1920px hiện tại |

## Kết quả kiểm tra mới bằng mã

- index.html giữ đúng SHA-256 đã công bố: 4a4aebb09a52f89a9d0dc04fa0a8d6e63b412982d9da9cb285b90d0df7d395ce.
- Fixture: 22 section, 1130 text layer. HTML mới: 22 phần tử data-section, 30 sản phẩm, 1 H1, 24 H2, 186 H3.
- Không thiếu chuỗi chữ nguồn theo phép so sánh bỏ khoảng trắng, tính cả placeholder. Đây là kiểm tra có mặt của chuỗi, chưa chứng minh số lần xuất hiện, thứ tự, khả năng nhìn thấy hoặc chữ nằm sẵn trong bitmap.
- Không thiếu tài nguyên src/href local trực tiếp trong HTML. Chưa phải kiểm kê toàn bộ dependency lồng trong CSS/SVG.
- HTML5 parser: 0 lỗi.
- Render header, section và footer trong bộ nhớ rồi chuẩn hóa khoảng trắng cuối dòng cho kết quả khớp HTML đang lưu. Không chạy main() hoặc ghi đè index2.html.

## Vấn đề và mức ưu tiên

### P1 — Bố cục thân trang chưa được chuyển theo từng section

render_section() dùng content-grid/content-card chung, trong khi nguồn có 20 nhóm thân trang khác nhau về phân cấp, nền, ảnh, bố trí và nhịp chữ. index2.css dùng nền trắng, border và heading chung. Giữ đủ 1130 chuỗi không chứng minh fidelity. Cần template/style riêng cho từng nhóm hoặc họ bố cục thực sự tương đồng, dùng desktop geometry để dựng desktop và mobile pieces để dựng responsive.

### P1 — Header còn sai lệch có bằng chứng

section-1-visual-guide.md ghi MAE toàn section 14,74/255; utility 30,58; menu 22,91; nav 23,02. Đây là số đo snapshot lưu sẵn. Đã mở trực tiếp section-overlay.png: chữ, icon, pill và CTA bị lệch giữa hai lớp. Ưu tiên utility/menu/nav, sau đó logo/search/account/benefits, rồi ba banner. Giữ điều kiện đo gốc: khung section 1920 × 1043, DPR 1, font và ảnh tải xong. Mục tiêu đề xuất trong guide là lệch hình học/baseline tối đa 1 CSS px; chưa được nghiệm thu.

### P1 — Báo cáo và công cụ cũ không đồng bộ với mã mới

INDEX2-AUDIT.md và HEADER-HTML-AUDIT.md nêu chiều cao khớp tuyệt đối, heading 48/51 H3 và điểm Lighthouse 96/92 accessibility. Bản hiện tại có 186 H3 và renderer đã đổi. tools/index2/README.md còn nói build gọi normalize-header.py và sinh token; NATIVE-HTML.md cùng code hiện tại xác nhận không còn tuyến đó. Không chạy write-index2-report.py/audit-header.py để xuất lại báo cáo nếu chưa cập nhật phép đo và giả định.

final-index2-audit.py tính newCodeBytes chỉ từ HTML, index2.css, index2.js, bỏ index2-header.css; kiểm font theo fonts.css cũ thay vì dependency thực tế. Báo cáo dung lượng của tuyến kiểm tra này chưa đủ cho bản hiện tại. Các kiểm tra text dùng substring không xác nhận vị trí hay số lần xuất hiện.

### P2 — Hero có giới hạn asset nguồn

hero-clean.webp được phục dựng từ PNG có chữ bằng inpainting/làm mờ. Không có nền sạch gốc để đảm bảo khớp pixel. HTML dựng lại chữ và lớp kính; cần tách sai lệch nền khỏi sai lệch hình học/text. Xin asset sạch khi cần nghiệm thu chính xác; sửa CSS không phục hồi được texture gốc đã mất.

### P2 — Chuẩn hóa semantic và tương tác còn cần kiểm

186 H3 xuất phát từ quy tắc suy đoán theo tên layer và dòng đầu của card, cần duyệt theo ý nghĩa nội dung. Filter chỉ đổi aria-pressed; mua hàng tăng bộ đếm trong bộ nhớ; tìm kiếm/newsletter thông báo demo; video chưa phát nội dung thực. Hero pagination hiện là phần tử trang trí aria-hidden. Các mô tả chức năng cũ phải được kiểm lại theo mã này. Consent newsletter được checked sẵn; cần quyết định theo yêu cầu sản phẩm khi triển khai thật.

### P2 — Bộ lệnh browser lưu sẵn cần rà lại tính cô lập

chrome-mcp-check.py dùng đúng managed launcher, nhưng có thể chọn tab có URL khớp đã tồn tại. Trước khi chạy lại cần tạo URL/tab riêng của tác vụ và xác nhận ownership, tránh chọn nhầm tab tác vụ khác. Chỉ dùng Chrome DevTools MCP qua launcher chuyên dụng theo AGENTS; không dùng backend khác khi lỗi kết nối.

## Thứ tự triển khai tiếp

1. Giữ index.html và assets nguồn làm chuẩn; ghi commit/hash vào mỗi đợt bằng chứng mới.
2. Đồng bộ tài liệu/công cụ với tuyến native hiện tại; phân biệt dữ liệu build, chứng cứ lịch sử và kết quả hiện tại.
3. Hoàn thiện section 01 theo tám vùng của visual guide; sửa template trong build-index2.py và style tại index2-header.css.
4. Chuyển section 02–21 theo từng bố cục nguồn; làm footer riêng. Sau mỗi nhóm, build rồi kiểm desktop/mobile, text, asset và tương tác.
5. Chụp source/current cùng viewport, DPR và readiness. Với mobile rất dài, dùng tile để tránh lỗi compositor. Duyệt overlay và diff theo từng vùng, không nghiệm thu chỉ bằng MAE.
6. Chạy lại parse, resource, heading, keyboard, no-JS, responsive và Lighthouse trên đúng commit sau cùng; cập nhật báo cáo bằng kết quả mới.
