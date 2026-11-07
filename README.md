# HACOM V2 2026

Mở `index.html` trong Chrome. Trang dùng HTML, Tailwind CDN và SVG tách theo 22 section. Ảnh và font được tải từ thư mục cục bộ. Dữ liệu tương tác chỉ phục vụ demo.

## Nguồn thiết kế

- Frame `43:3` từ Figma Design, tên “HACOM Website Desktop / 1920px”.
- Bản xuất SVG giữ chữ dạng text. Giữ các tọa độ, layer, mặt nạ, tỉ lệ ảnh và thông số typography theo file xuất.
- 170 file ảnh gốc được tách ra từ SVG, không thay ảnh theo danh mục. Sáu font được nạp cục bộ: Inter, Goldman, Roboto Slab, Manrope, Roboto Condensed và Roboto.
- `build-fidelity.py` tạo lại các script dữ liệu từ ZIP do Figma xuất. Chạy `python build-fidelity.py <zip> --fonts-dir <node_modules>` với các gói Fontsource tương ứng.
- Bản triển khai trước được lưu ở `reference/previous-index.html` để đối chiếu mã nguồn.

## Quy tắc hiển thị

Desktop 1920px dùng tọa độ của frame gốc, với tổng chiều cao 20.142px theo SVG. Frame rộng tối đa 1920px trên màn hình lớn. Các nhóm nội dung rộng 1856px trong thiết kế gốc, nên lựa chọn ưu tiên khớp frame 1920px thay thế giới hạn nội dung 1800px của bản demo trước.

Dưới 1024px, các nhóm có layer độc lập xếp lại theo chiều rộng. Ảnh artwork vẫn giữ tỷ lệ gốc, chữ nằm sẵn trong artwork sẽ co cùng ảnh. Các cụm rộng có layer chồng nhau giữ nguyên bố cục và có vùng cuộn cục bộ. Các lớp backdrop blur, fill, shadow, mask và ảnh gốc của SVG được giữ trên desktop. Trình duyệt và Figma có thể raster hóa chữ khác nhau.

## Bằng chứng nghiệm thu

- `reference/fidelity-source-checks.json` ghi nhận 22 nhóm, 1.130 layer chữ khớp nội dung và thuộc tính nguồn, 180 tham chiếu ảnh tới 170 file gốc.
- `reference/fidelity-desktop-checks.json` ghi kích thước từng nhóm và lỗi tài nguyên tại 1920px.
- `reference/fidelity-responsive-checks.json` ghi 12 viewport, thao tác menu, tìm kiếm, yêu thích, giỏ hàng và lỗi console.
- `reference/fidelity-mobile-sections.json` ghi kiểm tra 22 nhóm ở 390px và xác thực đăng ký demo.
- `reference/desktop-1920/` chứa ảnh render tại các mốc section. `reference/index-390.png` là ảnh phần đầu trang ở 390px.
