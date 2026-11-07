> **Báo cáo cập nhật:** [Header và banner HTML](HEADER-HTML-AUDIT.md). Báo cáo bên dưới lưu kết quả nền trước lần sửa header; điểm Lighthouse, số heading, dung lượng và ảnh section 01 mới nằm trong báo cáo cập nhật.

# Báo cáo nền index2.html — trước hiệu chỉnh header

## Kết quả

Đã viết lại nội dung thành HTML có ngữ nghĩa, dùng CSS/JavaScript riêng, bỏ Tailwind CDN và cơ chế tải nội dung SVG bằng JavaScript. Bản mới giữ đủ nội dung chữ của 1.130 layer nguồn, 22 nhóm nội dung và 30 thẻ sản phẩm dạng article trong danh sách. Icon/logo nhỏ giữ vector; artwork phức tạp được tách thành ảnh WebP lossless. Phép kiểm tra ban đầu chỉ bao phủ lớp chữ SVG và đã bỏ sót chữ có sẵn trong PNG banner chính; thiếu sót này được sửa trong bản hiệu chỉnh header.

**Nghiệm thu bố cục và chức năng:** đạt các kiểm tra dưới đây. **Không xác nhận trùng pixel 100%:** ảnh diff còn ghi nhận khác biệt ở đường biên chữ và raster hóa artwork. Các ảnh trước/sau, overlay và diff được lưu đầy đủ để kiểm tra trực tiếp; kết quả không được suy diễn thành “100% giống Figma”.

Không sửa index.html, fidelity.css, fidelity.js, assets/faithful hoặc các file triển khai cũ. SHA-256 của index.html: `4a4aebb09a52f89a9d0dc04fa0a8d6e63b412982d9da9cb285b90d0df7d395ce`.

## SEO và HTML

| Hạng mục | Bản gốc | index2.html |
|---|---|---|
| Title | HACOM V2 2026 | HACOM - Laptop, PC Gaming và thiết bị công nghệ |
| Description | HACOM V2 2026 | Mô tả ngành hàng và hệ thống showroom bằng tiếng Việt |
| Heading | Không có H1–H6 | 1 H1, H2 theo nhóm nội dung, 48 H3 cho sản phẩm/bài viết/video |
| Nội dung HTML ban đầu | 22 section rỗng | Toàn bộ nội dung có trong HTML |
| JavaScript để đọc nội dung | Cần tải và dựng SVG | Không cần; đã kiểm thử với CSP chặn script |
| Ngữ nghĩa | Nội dung chủ yếu là SVG | header, nav, main, section, footer, ul/li/article, form/label/input/button |
| Liên kết demo | Anchor # | Button cho hành động demo; liên kết liên hệ dùng đích đã có trong nguồn |
| Tài nguyên ngoài | Tailwind CDN | Không có script ngoài; font cục bộ |

- HTML5 parser: **0 lỗi**; không có ID trùng; không thiếu tài nguyên/font; không mất nội dung chữ gốc; không có button vô danh, ảnh thiếu alt hoặc anchor `href="#"`.
- H1 là câu giới thiệu HACOM đang hiển thị trên thanh đầu trang; không thêm heading SEO ẩn.
- Có 24 thẻ H2 trong source vì một số tiêu đề có hai cách trình bày responsive. CSS chỉ hiển thị cách trình bày phù hợp. Cấu trúc H1 → H2 → H3 được kiểm tra; giá, badge và nút không dùng heading.
- Ảnh artwork dùng `alt=""`/aria-hidden khi nội dung tương ứng đã có bằng chữ HTML. Icon và nền không được dùng để thay thế tên sản phẩm.
- Không tạo đánh giá/schema từ dữ liệu demo. Không truy cập GA, GTM, Search Console hoặc tài khoản ngoài.

### Nội dung gốc cần chủ sở hữu xác nhận

Giữ nguyên các điểm chưa đồng nhất để không đổi thiết kế: thanh đầu ghi 22+ showroom nhưng footer có 20+; prototype mang tên 2026 nhưng copyright là 2027. Thẻ laptop đầu tiên của nhóm Laptop ghi giảm 32% trong khi giá 39.990.000đ → 31.990.000đ tương ứng khoảng 20%. Các số liệu, giá và nhãn này chưa được xác minh như thông tin kinh doanh thật; không dùng chúng để sinh schema Product/Offer hoặc tự sửa nội dung hiển thị.

### Các mục cần dữ liệu triển khai production

Canonical, Open Graph URL/ảnh chia sẻ, URL chi tiết sản phẩm/danh mục, robots.txt, sitemap, HTTP status và khả năng index trên tên miền thật chưa được xác nhận bởi một file prototype local. Không tự đặt canonical cho index2.html hoặc bịa URL sản phẩm. Cần bổ sung các đích thật khi tích hợp vào website; các liên kết thương mại trong demo hiện là button. Chỉ dùng liên kết tel/mailto/website khi đích đã có trong nội dung gốc.

## Lighthouse trên HTTP local

| Thiết bị | SEO | Best Practices | Accessibility |
|---|---:|---:|---:|
| Desktop | 100 | 100 | 96 |
| Mobile | 100 | 100 | 96 |

Accessibility còn cảnh báo vùng bấm sát nhau khi thu nhỏ desktop và tương phản chữ trắng trên đỏ #ed1c24 (khoảng 4,38:1). Đã mở rộng vùng bấm trong suốt; không đổi kích thước hàng hoặc màu thương hiệu để chạy theo điểm số, vì yêu cầu giữ nguyên thị giác. Lighthouse 100 SEO không chứng minh trang sẽ được index hoặc xếp hạng trên production.

Chi tiết: [desktop](reference/index2-lighthouse/desktop/report.html), [mobile](reference/index2-lighthouse/mobile/report.html).

## Responsive và tương tác

| Viewport | Chiều cao gốc | Chiều cao mới | Lệch section lớn nhất | Overflow toàn trang |
|---:|---:|---:|---:|---:|
| 360 | 62310 | 62310 | 0.00px | 0px |
| 390 | 62132 | 62132 | 0.00px | 0px |
| 768 | 45130 | 45130 | 0.00px | 0px |
| 1023 | 10734 | 10734 | 0.00px | 0px |
| 1024 | 10742 | 10742 | 0.00px | 0px |
| 1280 | 13428 | 13428 | 0.00px | 0px |
| 1440 | 15107 | 15107 | 0.00px | 0px |
| 1920 | 20142 | 20142 | 0.00px | 0px |
| 2560 | 20142 | 20142 | 0.00px | 0px |
| 3440 | 20142 | 20142 | 0.00px | 0px |

- Desktop 1920px: khung tối đa 1920px, tổng chiều cao **20.142px**.
- Đã kiểm tra chuỗi thay kích thước 1920 → 390 → 768 → 1024 → 360 → 1920, gồm chuyển qua breakpoint. Chế độ xuống dòng của bản gốc được chọn khi vào mobile và được giữ khi đổi giữa các kích thước mobile; bản mới giữ hành vi này bằng trạng thái CSS nhỏ, không tải hoặc dựng lại nội dung.
- Tìm kiếm, yêu thích bật/tắt, giỏ hàng, bộ lọc, carousel, menu mở/đóng, Escape trả focus: đã kiểm tra.
- Newsletter: dữ liệu sai bị từ chối; email/số điện thoại hợp lệ được nhận; checkbox đồng ý là bắt buộc.
- Đã dùng Chrome DevTools MCP gửi Space và Enter thật để kiểm tra favorite và submit tìm kiếm.
- CSP `script-src 'none'`: đủ 22 section, heading và chữ HTML; chiều cao desktop vẫn 20.142px. Các tương tác demo ngừng chạy đúng như dự kiến.

## Đối chiếu hình ảnh

- 1920px: 22 cặp ảnh; sai số màu trung bình có trọng số **1.638/255**. Không có cặp ảnh trùng pixel tuyệt đối.
- 390px: 22 cặp ảnh; sai số màu trung bình có trọng số **2.541/255**. Không có cặp ảnh trùng pixel tuyệt đối.

Ảnh từng section nằm ở `reference/index2-visual/1920/` và `reference/index2-visual/390/`: `before-NN.webp`, `after-NN.webp`, `overlay-NN.webp`, `diff-NN.webp`. Ảnh được chụp ở DPR 1, cùng Chrome/profile và viewport. Mobile được chụp theo tile 1080px rồi ghép, để tránh lỗi compositor khi chụp trang dài hơn 62.000px. Diff gồm cả khác biệt anti-aliasing/subpixel; không dùng một ngưỡng tùy ý để tuyên bố đạt 100%.

## Dung lượng và đo tải

| Hạng mục | Bản gốc | Bản mới |
|---|---:|---:|
| HTML/CSS/JS riêng của trang, chưa gzip | 1,542,084 B | 545,232 B |
| Đồ họa/ảnh, không tính font dùng chung | 130,815,463 B | 34,619,463 B |

Mã trang giảm **64.6%**; tài nguyên đồ họa được tham chiếu giảm **73.5%**. Bản mới tránh nhân đôi cây SVG và dùng content-visibility cho phần ngoài màn hình desktop; nội dung vẫn có sẵn trong HTML.

Một lần đo local tại 1920px, không throttling: bản gốc FCP 156ms, LCP 372ms, 40 request/23,220,914 B; bản mới FCP 440ms, LCP 440ms, 18 request/1,757,827 B. Đây là đo lab một lần trên máy đang chạy kiểm thử, cache và đối tượng LCP khác nhau; **không khẳng định mọi thời điểm render nhanh hơn**. Số node ở lần tải đầu không tương đương vì bản gốc mới tải một phần nội dung; so sánh DOM đầy đủ nằm trong JSON ma trận.

## Mở và bảo trì

Mở index2.html trực tiếp hoặc chạy `python -m http.server 8765 --bind 127.0.0.1` tại thư mục dự án và truy cập `http://127.0.0.1:8765/index2.html`. Không cần build để xem.

index2.html là HTML đầu ra đầy đủ; index2.css chứa style thành phần và token chữ dùng chung; index2.js chỉ giữ demo interaction và lựa chọn chế độ reflow khi qua breakpoint. `build-index2.py` tái tạo HTML/token từ thông số tham chiếu đã đo. Ảnh mới nằm riêng trong assets/index2. Không chạy build-fidelity.py để chỉnh bản mới.

Các bằng chứng máy đọc được: `reference/index2-static-audit.json`, `reference/index2-matrix-results.json`, `reference/index2-breakpoint-results.json`, `reference/index2-interaction-results.json`, `reference/index2-keyboard-results.json`, `reference/index2-nojs-results.json`, `reference/index2-load-results.json`, `reference/index2-visual-results.json`.
