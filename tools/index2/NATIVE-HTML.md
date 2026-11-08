# Index2 — giao diện HTML/CSS

Chạy `python build-index2.py` để sinh lại `index2.html` từ fixture nội dung trong `reference/`. Mở trang qua HTTP local, ví dụ `python -m http.server 8765`, rồi truy cập `/index2.html`. Bộ sinh dùng thư viện chuẩn Python và chỉ ghi trang HTML. CSS và JavaScript được sửa trực tiếp.

## Ánh xạ section

| Section | Thành phần hiện tại |
|---|---|
| 01 · Header | Thanh thông tin, logo, form tìm kiếm, thao tác tài khoản, danh sách điều hướng, menu danh mục, hero, ba khuyến mại và bảy cam kết dịch vụ |
| 02 · Ngành hàng nổi bật | Lưới thẻ ngành hàng và khối PC Builder |
| 03 · Flash Sale | Khối ưu đãi, nhóm danh mục và carousel sản phẩm |
| 04 · Chọn đúng máy | Lưới thẻ nhu cầu công việc |
| 05 · Laptop | Nhóm ưu đãi và carousel sản phẩm |
| 06 · PC | Thẻ ngành hàng và carousel sản phẩm |
| 07 · PC Builder | Khối nội dung, lợi ích và CTA |
| 08 · Màn hình | Bộ lọc, thẻ nội dung và carousel sản phẩm |
| 09 · Linh kiện | Lưới linh kiện và banner nội dung |
| 10 · Gaming Gear | Lưới phụ kiện và banner nội dung |
| 11 · Console | Lưới nhóm thiết bị giải trí |
| 12 · Mạng | Lưới nhóm thiết bị và nút khám phá |
| 13 · Thiết bị văn phòng | Nhóm ngành hàng, bộ lọc và carousel sản phẩm |
| 14 · Nhà thông minh | Thẻ thiết bị và thông tin nhà thông minh |
| 15 · Doanh nghiệp | Thông tin giải pháp và logo đối tác |
| 16 · Dịch vụ | Thông tin sửa chữa và nhóm dịch vụ |
| 17 · Số liệu | Các thẻ số liệu và hình minh họa |
| 18 · Tin công nghệ | Thẻ nội dung và bộ lọc demo |
| 19 · Video | Carousel thẻ video |
| 20 · Khách hàng | Carousel thẻ nội dung khách hàng |
| 21 · Kênh mua sắm | Lưới thẻ khuyến mại và CTA |
| 22 · Footer | Newsletter, chỉ số, showroom, nhóm liên kết và thông tin liên hệ |

`content-images.json` ánh xạ ảnh nguồn sang ảnh nội dung có kích thước xác định. Tệp WebP trong `assets/index2/content/` là biến thể giảm dung lượng của ảnh nguồn. `product-photos.json` ánh xạ 30 mã thẻ sang vùng ảnh sản phẩm tách từ dữ liệu cũ. Hero dùng ảnh laptop độc lập và gradient CSS. Hai ảnh menu/cam kết và ảnh ghép nguyên header đã được gỡ khỏi đường render.

Các snapshot và script kiểm tra fidelity đời trước được giữ để đối chiếu. Quy trình sinh trang hiện tại đọc fixture, dựng component và xuất HTML, nên không chạy `normalize-header.py`. Các thao tác thương mại và phát video vẫn ở chế độ demo.
