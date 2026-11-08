# Audit thị giác section-1

Chuẩn duy nhất là section đầu tiên trong [index.html](../index.html). Bản cần hiệu chỉnh là [index2.html](../index2.html). Các bảng dưới đây dùng tọa độ CSS px theo gốc section, theo thứ tự **x, y, rộng, cao**. Số đo ảnh và số đo trình duyệt được ghi riêng.

## Điều kiện đo và bằng chứng

Hai trang được chụp liên tiếp trong cùng Chrome 156.0.8078.80 qua HTTP local, viewport 2555 × 1047, DPR 1, zoom 100%, ẩn thanh cuộn. Chờ section SVG có `data-loaded=true`, font sẵn sàng và giải mã thành công 6 ảnh của mỗi trang. Cả hai section ở **(317,5; 0) trên màn hình**, kích thước **1920 × 1043**.

- Ảnh viewport gốc: [index](section-1-audit/index-viewport.png) · [index2](section-1-audit/index2-viewport.png).
- Ảnh toàn section: [chuẩn](section-1-audit/section-source.png) · [hiện tại](section-1-audit/section-current.png) · [overlay 50%](section-1-audit/section-overlay.png) · [diff](section-1-audit/section-diff.png).
- Dữ liệu phần tử: [SVG](section-1-audit/index.json) · [HTML](section-1-audit/index2.json) · [bảng chữ và baseline](section-1-audit/text-comparison.csv). JSON chứa hộp màn hình và hộp tương đối, computed style, thuộc tính gốc, path, stroke, transform và danh mục ảnh kèm kích thước nội tại. CSV ghép nhãn trùng theo vị trí gần nhất, cần kiểm tra thủ công với nhãn lặp, nhãn ghép hoặc chữ nằm trong ảnh. Baseline SVG trong JSON là tọa độ màn hình của ký tự đầu. Baseline HTML được lấy bằng mốc inline cao 0 cho nút hoặc đoạn chữ đơn giản.
- Mỗi vùng có bộ `<vùng>-source/current/overlay/diff.png` trong [thư mục bằng chứng](section-1-audit/). Crop dùng cùng gốc pixel x=318 và cùng biên cho cả hai ảnh. Không áp dụng dịch chuyển riêng hoặc đổi kích thước.

## Đối chiếu tám vùng

| Vùng và bằng chứng | Chuẩn SVG | HTML hiện tại | Việc cần sửa |
|---|---|---|---|
| Thanh thông tin · [diff](section-1-audit/utility-diff.png) | Nền (0, 0, 1920, 50), #0D1017. Vương miện tại (33, 15, 22, 20). Bốn pill bắt đầu x=564, 730, 856, 982, cùng y=8, h=34, radius 17. | `.utility` đúng hộp ngoài. Hàng nút chia khoảng bằng Flex, vương miện dùng hộp SVG 25 px. MAE RGB 30,58. | Ưu tiên cao. Lấy hộp từng pill và nhóm bên phải từ SVG. Dùng lưới có cột và khoảng cách đo được. Khôi phục màu nền, path vương miện, nhịp chữ và các đường phân cách. |
| Logo · [diff](section-1-audit/logo-diff.png) | `Logo HACOM 1` tại (32, 92, 162,89, 62). | Ảnh trong `.brand` dùng cùng PNG nhưng tại (32, 93,55, 160, 60,89). | Chỉnh kích thước và trục dọc của ảnh, sau đó đo từng baseline của chữ cạnh logo từ các tspan. |
| Tìm kiếm · [diff](section-1-audit/search-diff.png) | Nhóm `Search` tại (392, 99, 899, 50), radius 25. Nút tại (1171, 99, 120, 50). Icon `search` có hộp nét 18 × 18 tại (415, 115). | `.search` tại (392, 99, 898, 50). | Chốt rộng 899 ở khung chuẩn. Đo padding từ hộp nét và baseline chữ gợi ý. Lấy path kính lúp, camera và mic từ SVG. |
| Tài khoản · [diff](section-1-audit/account-diff.png) | Hộp nét `user-round` (1464, 99,75, 20, 22,5), `heart` (1574,5, 100,98, 25, 21,27), `shopping-cart` (1781,56, 98,56, 25,05, 24,94). | `.account` là hàng Flex trong hộp (1310, 94,75, 578, 58,5), các icon chia chung hộp 26 px. | Trích path từng icon, đo tâm nét và baseline nhãn của cả bốn nút. Căn các đường phân cách độc lập với hộp hit. |
| Menu · [diff](section-1-audit/menu-diff.png) | Nền (32, 176, 276, 721), radius 20. Đầu menu cao 50, màu #E72429. Hàng nổi bật tại (40, 393, 260, 30), radius 15. | `.departments` tại (32, 176, 276, 720,80). Icon và nền dùng định nghĩa riêng. MAE 22,91. | Giữ hộp ngoài, sửa lần lượt hộp và baseline từng hàng. So lại path, nét phân cách, vị trí chevron, fill và bóng. |
| Điều hướng nhanh · [diff](section-1-audit/nav-diff.png) | Nhóm `Nav item Flash Sale` tại (356,21, 184,32, 102,97, 20), `Nav item Laptop AI` tại (529,12, 184,32, 101,55, 20). | `.quick-nav` tại (328, 176, 1560, 50), các mục chia Flex. Hai nhãn đầu có baseline khoảng 201, so với 200,318 của SVG. MAE 23,02. | Giữ typography đã căn, thay phân phối theo nội dung bằng các mốc nhóm đo từ SVG. So tiếp divider, icon và pill Build PC. |
| Hero và ba banner · [diff](section-1-audit/banners-diff.png) · [hero](section-1-audit/hero-diff.png) | Hero (328, 226, 1031, 671). Ba banner x=1379, y=226/456/686, h=210/210/211, radius 20. CTA Gaming tại (1394,32, 852,29, 140, 29,17). | Hero đúng hộp. Banner cao khoảng 210,33 mỗi tấm, y=226/456,33/686,66, radius 18. CTA Gaming rộng khoảng 125,52. | Dùng ba hàng 210/210/211 ở desktop chuẩn, radius 20. Đặt chiều rộng CTA theo SVG, tách mũi tên thành SVG riêng. Đối chiếu crop và logo NVIDIA trước khi chỉnh nền. |
| Bảy cam kết · [diff](section-1-audit/services-diff.png) | Nền (32, 917, 1856, 80), radius 20. Nét `truck` tại (85, 942,5, 33,34, 26,66). Hai baseline đầu là 953,318 và 974,364. | `.benefits` đúng hộp. Hai baseline đầu khoảng 953 và 974. Icon dùng SVG tự dựng 36 × 36. | Giữ nhịp chữ đầu đã khớp. Đo các đường chia cột và tâm icon còn lại, rồi thay path theo nguồn. |

MAE là trung bình sai số tuyệt đối trên ba kênh RGB, thang 0–255. Toàn section là **14,74**. MAE dùng để ưu tiên kiểm tra, còn nghiệm thu dựa trên từng mốc hình học, chữ và asset. Khác biệt do bóng, nền, crop và khử răng cưa có thể xuất hiện ngay cả khi hộp đã đúng.

## Cách sửa từ nguồn

1. **Hình học.** Trong Chrome, tìm `section[data-section="1"] .section-art`. Đọc [01.js](../assets/faithful/01.js) và [fidelity.js](../fidelity.js) để theo từ group đến hình thực sự vẽ. Với SVG, dùng `getBBox()` và đưa các góc qua `getScreenCTM()`. Đối với nét và bóng, kiểm thêm thuộc tính stroke/filter và ảnh chụp vì hộp hình học không bao trọn hiệu ứng. Trừ tọa độ gốc section trước khi so với `getBoundingClientRect()` của HTML.
2. **Ảnh và crop.** Theo `fill="url(#…)"` qua pattern và image. Ba ảnh gốc banner là PNG 1539 × 630, mã lần lượt `76dee67fa59b399a4b6d51fd`, `70770a858c633c940eb12aa0`, `3b1cac963ffdb2c1fedecbe5`. Bản hiện tại dùng WebP 840 × 344 và `object-fit: cover`. Đối chiếu transform pattern với crop HTML. Nếu WebP vẫn khác đáng kể sau khi căn crop, dùng PNG gốc để đo tách ảnh hưởng nén. Logo HACOM và NVIDIA đang dùng PNG gốc 289 × 110 và 448 × 135.
3. **Typography.** Dùng Inter và các subset khai báo trong [fonts.css](../assets/faithful/fonts.css). So computed font và kiểm bằng DevTools → Rendered Fonts, nhất là chữ tiếng Việt. Lấy baseline SVG từ `getStartPositionOfChar()` sau khi áp dụng CTM. Đo HTML bằng một mốc inline cao 0 cạnh chữ. Chỉnh weight, size và tracking trước, rồi chỉnh padding, khoảng cách hàng và line-height theo baseline thực. Khoảng cách baseline của SVG chỉ là số đo vị trí, nên line-height CSS phải được xác định từ cách font render.
4. **Icon và trang trí.** Sao chép path và transform từ group SVG tương ứng. Giữ fill, stroke, width, linecap, linejoin và fill-rule. Đưa icon về viewBox riêng bằng cách dịch gốc, giữ tỷ lệ và đối chiếu hộp nét sau khi render. Với các khối bo góc, dùng `rx/ry` của rect nguồn sau khi tính transform. Đo hiệu ứng từ filter và opacity gốc trước khi chỉnh shadow, blur hoặc gradient trong CSS.
5. **Nơi sửa.** Chỉnh layout, chữ và hiệu ứng tại [index2-header.css](../index2-header.css). Chỉnh markup, icon, asset và nhãn nút tại `render_header()` trong [build-index2.py](../build-index2.py). Sau thay đổi template, chạy `python build-index2.py` để sinh lại HTML rồi chụp lại cùng điều kiện.

### Giới hạn của hero

SVG dùng PNG `fcfdbbb19fa8a366fc216a4b.png` (1035 × 663). PNG đã ghép sẵn một phần chữ và giao diện. Bản HTML dùng ảnh `hero-clean.webp` cùng kích thước, tạo bằng inpainting và làm mờ trong [prepare-header-art.py](../tools/index2/prepare-header-art.py). Phần ảnh điền lại và lớp kính CSS tạo sai lệch quanh vùng chữ, ô lợi ích và nhãn RTX. Xem [overlay hero](section-1-audit/hero-overlay.png) và [diff hero](section-1-audit/hero-diff.png).

Đo nút, nội dung HTML và các hình có tọa độ SVG độc lập trước. Đối với phần đã ghép trong PNG, ghi mốc đo từ raster và độ bất định do chữ hoặc mép mờ. Ghi riêng phần nền cần asset sạch để có thể khớp từng pixel.

## Kiểm tra hồi quy và checklist nghiệm thu

- [x] Đã đo bản HTML tại **390, 820, 1024, 1280 và 1920 px**. Chiều rộng tài liệu bằng viewport ở cả năm mốc. Vùng cam kết tăng chiều cao lên 310 px tại 390, và 190 px ở ba mốc tablet/desktop nhỏ. Hai CTA “Xem ngay” cao 44 px dưới 1440, còn 30 px ở 1920 theo bố cục desktop. Dữ liệu hộp điều khiển nằm trong [responsive.json](section-1-audit/responsive.json). Việc không tràn tài liệu chưa xác nhận từng dòng không bị cắt.
- [x] Chặn ảnh raster rồi tải lại. Không có ảnh nào giải mã trong header, menu vẫn mở, form tìm kiếm vẫn phát sự kiện submit, 33 nút và 7 mục cam kết vẫn có mặt. Đây là kiểm tra khói, chưa thử từng nút và mọi đường đi bàn phím. [Kết quả](section-1-audit/no-images.json).
- [ ] Sửa thanh thông tin, menu và điều hướng trước. Sau đó căn logo, ô tìm kiếm, nhóm tài khoản và cam kết.
- [ ] Căn ba banner và CTA, rồi tách riêng phần sai khác do ảnh hero đã phục dựng.
- [ ] Chụp lại hai trang. Kiểm mốc hình học và baseline lệch tối đa **1 CSS px**, font và số dòng đúng nguồn, thứ tự menu khớp. Mở overlay theo từng vùng để xác nhận icon, màu, crop và bóng.
- [ ] Sau mỗi lượt sửa, kiểm tra các viewport trên để phát hiện cắt chữ, xuống dòng ngoài dự kiến và nút bị co. Kiểm lại menu bằng bàn phím, form và CTA khi ảnh không tải.
