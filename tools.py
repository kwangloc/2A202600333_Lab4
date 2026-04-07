from langchain_core.tools import tool

from typing import List

# =====================================================================
# MOCK DATA Dữ liệu giả lập hệ thống du lịch
# Sinh viên cần đọc hiểu data để debug test cases.
# =====================================================================

FLIGHTS_DB = {
    ("Hà Nội", "Đà Nẵng"): [
        {
            "airline": "Vietnam Airlines",
            "departure": "06:00",
            "arrival": "07:20",
            "price": 1_450_000,
            "class": "economy",
        },
        {
            "airline": "Vietnam Airlines",
            "departure": "14:00",
            "arrival": "15:20",
            "price": 2_800_000,
            "class": "business",
        },
        {
            "airline": "VietJet Air",
            "departure": "08:30",
            "arrival": "09:50",
            "price": 890_000,
            "class": "economy",
        },
        {
            "airline": "Bamboo Airways",
            "departure": "11:00",
            "arrival": "12:20",
            "price": 1_200_000,
            "class": "economy",
        },
    ],

    ("Hà Nội", "Phú Quốc"): [
        {
            "airline": "Vietnam Airlines",
            "departure": "07:00",
            "arrival": "09:15",
            "price": 2_100_000,
            "class": "economy",
        },
        {
            "airline": "VietJet Air",
            "departure": "10:00",
            "arrival": "12:15",
            "price": 1_350_000,
            "class": "economy",
        },
        {
            "airline": "VietJet Air",
            "departure": "16:00",
            "arrival": "18:15",
            "price": 1_100_000,
            "class": "economy",
        },
    ],

    ("Hà Nội", "Hồ Chí Minh"): [
        {
            "airline": "Vietnam Airlines",
            "departure": "06:00",
            "arrival": "08:10",
            "price": 1_600_000,
            "class": "economy",
        },
        {
            "airline": "VietJet Air",
            "departure": "07:30",
            "arrival": "09:40",
            "price": 950_000,
            "class": "economy",
        },
        {
            "airline": "Bamboo Airways",
            "departure": "12:00",
            "arrival": "14:10",
            "price": 1_300_000,
            "class": "economy",
        },
        {
            "airline": "Vietnam Airlines",
            "departure": "18:00",
            "arrival": "20:10",
            "price": 3_200_000,
            "class": "business",
        },
    ],

    ("Hồ Chí Minh", "Đà Nẵng"): [
        {
            "airline": "Vietnam Airlines",
            "departure": "09:00",
            "arrival": "10:20",
            "price": 1_300_000,
            "class": "economy",
        },
        {
            "airline": "VietJet Air",
            "departure": "13:00",
            "arrival": "14:20",
            "price": 780_000,
            "class": "economy",
        },
    ],

    ("Hồ Chí Minh", "Phú Quốc"): [
        {
            "airline": "Vietnam Airlines",
            "departure": "08:00",
            "arrival": "09:00",
            "price": 1_100_000,
            "class": "economy",
        },
        {
            "airline": "VietJet Air",
            "departure": "15:00",
            "arrival": "16:00",
            "price": 650_000,
            "class": "economy",
        },
    ],
}

HOTELS_DB = {
    "Đà Nẵng": [
        {
            "name": "Mường Thanh Luxury",
            "stars": 5,
            "price_per_night": 1_800_000,
            "area": "Mỹ Khê",
            "rating": 4.5,
        },
        {
            "name": "Sala Danang Beach",
            "stars": 4,
            "price_per_night": 1_200_000,
            "area": "Mỹ Khê",
            "rating": 4.3,
        },
        {
            "name": "Fivitel Danang",
            "stars": 3,
            "price_per_night": 650_000,
            "area": "Sơn Trà",
            "rating": 4.1,
        },
        {
            "name": "Memory Hostel",
            "stars": 2,
            "price_per_night": 250_000,
            "area": "Hải Châu",
            "rating": 4.6,
        },
        {
            "name": "Christina's Homestay",
            "stars": 2,
            "price_per_night": 350_000,
            "area": "An Thượng",
            "rating": 4.7,
        },
    ],

    "Phú Quốc": [
        {
            "name": "Vinpearl Resort",
            "stars": 5,
            "price_per_night": 3_500_000,
            "area": "Bãi Dài",
            "rating": 4.4,
        },
        {
            "name": "Sol by Meliá",
            "stars": 4,
            "price_per_night": 1_500_000,
            "area": "Bãi Trường",
            "rating": 4.2,
        },
        {
            "name": "Lahana Resort",
            "stars": 3,
            "price_per_night": 800_000,
            "area": "Dương Đông",
            "rating": 4.0,
        },
        {
            "name": "9Station Hostel",
            "stars": 2,
            "price_per_night": 200_000,
            "area": "Dương Đông",
            "rating": 4.5,
        },
    ],

    "Hồ Chí Minh": [
        {
            "name": "Rex Hotel",
            "stars": 5,
            "price_per_night": 2_800_000,
            "area": "Quận 1",
            "rating": 4.3,
        },
        {
            "name": "Liberty Central",
            "stars": 4,
            "price_per_night": 1_400_000,
            "area": "Quận 1",
            "rating": 4.1,
        },
        {
            "name": "Cochin Zen Hotel",
            "stars": 3,
            "price_per_night": 550_000,
            "area": "Quận 3",
            "rating": 4.4,
        },
        {
            "name": "The Common Room",
            "stars": 2,
            "price_per_night": 180_000,
            "area": "Quận 1",
            "rating": 4.6,
        },
    ],
}


# Tools for agent
@tool
def search_flights(origin: str, destination: str) -> str:
    """
    Tìm kiếm và liệt kê các chuyến bay giữa hai thành phố, sắp xếp theo giá từ rẻ đến đắt.
    
    Dùng tool này khi khách hàng:
    - Muốn biết các chuyến bay khả dụng giữa hai thành phố
    - Muốn so sánh giá vé máy bay
    - Cần lên kế hoạch ngân sách cho vé máy bay

    Tham số:
        origin: thành phố khởi hành (VD: 'Hà Nội', 'Hồ Chí Minh', 'Đà Nẵng', 'Phú Quốc')
        destination: thành phố đến (VD: 'Đà Nẵng', 'Phú Quốc', 'Hồ Chí Minh', 'Hà Nội')

    Trả về:
        Danh sách chuyến bay được sắp xếp từ rẻ đến đắt, với thông tin:
        - Hãng hàng không (ví dụ: Vietnam Airlines, VietJet Air)
        - Giờ khởi hành và đến
        - Giá vé (VNĐ)
        - Hạng ghế (economy, business)
        
        Lưu ý: Nếu không tìm thấy tuyến bay trực tiếp, hãy cố gắng đảo ngược thứ tự các thành phố.
    """

    def format_price(price: int) -> str:
        return f"{price:,}".replace(",", ".") + "₫"

    # Tra cứu trực tiếp
    flights = FLIGHTS_DB.get((origin, destination))

    # Nếu không có, thử tra ngược
    reversed_route = False
    if not flights:
        flights = FLIGHTS_DB.get((destination, origin))
        reversed_route = True

    # Nếu vẫn không có
    if not flights:
        return f"Không tìm thấy chuyến bay từ {origin} đến {destination}."

    # Sắp xếp theo giá tăng dần (từ rẻ đến đắt)
    flights = sorted(flights, key=lambda x: x["price"])

    # Format kết quả
    result = []

    for flight in flights:
        result.append(
            f"- {flight['airline']} | "
            f"{flight['departure']} → {flight['arrival']} | "
            f"{format_price(flight['price'])} | "
            f"{flight['class']}"
        )

    route_note = ""
    if reversed_route:
        route_note = " (tuyến bay ngược)"

    return (
        f"Các chuyến bay từ {origin} đến {destination}{route_note}:\n"
        + "\n".join(result)
    )

@tool
def search_hotels(city: str, max_price_per_night: int = 99_999_999) -> str:
    """
    Tìm kiếm và liệt kê khách sạn tại một thành phố, lọc theo ngân sách và sắp xếp từ rẻ đến đắt.
    
    Dùng tool này khi khách hàng:
    - Muốn tìm khách sạn trong thành phố đích
    - Có ngân sách hạn chế cho chỗ ở
    - Muốn so sánh khách sạn theo giá
    - Cần lựa chọn giữa các mức độ sao và chất lượng

    Tham số:
        city: tên thành phố (VD: 'Đà Nẵng', 'Phú Quốc', 'Hồ Chí Minh')
                   Các thành phố có dữ liệu: Đà Nẵng, Phú Quốc, Hồ Chí Minh
        max_price_per_night: giá tối đa mỗi đêm (VNĐ), mặc định không giới hạn.
                            Dùng đây để lọc khách sạn theo ngân sách của khách hàng.

    Trả về:
        Danh sách khách sạn được lọc theo giá tối đa và sắp xếp từ rẻ đến đắt, với thông tin:
        - Tên khách sạn
        - Số sao (1-5 sao)
        - Khu vực/Địa điểm nằm trong thành phố
        - Giá mỗi đêm (VNĐ)
        - Đánh giá/Rating từ khách hàng
        
        Nếu không có khách sạn nào phù hợp với ngân sách, cân nhắc tăng max_price_per_night.
    """

    def format_price(price: int) -> str:
        return f"{price:,}".replace(",", ".") + "₫"

    # Kiểm tra thành phố có tồn tại không
    hotels = HOTELS_DB.get(city)
    if not hotels:
        return f"Không tìm thấy dữ liệu khách sạn tại {city}."

    # Lọc theo giá
    filtered_hotels = [
        h for h in hotels if h["price_per_night"] <= max_price_per_night
    ]

    # Nếu không có kết quả
    if not filtered_hotels:
        return (
            f"Không tìm thấy khách sạn tại {city} với giá dưới "
            f"{format_price(max_price_per_night)}/đêm. Hãy thử tăng ngân sách."
        )

    # # Sắp xếp theo rating giảm dần
    # filtered_hotels.sort(key=lambda x: x["rating"], reverse=True)

    # Sắp xếp theo giá tăng dần (từ rẻ đến đắt)
    filtered_hotels.sort(key=lambda x: x["price_per_night"])

    # Format kết quả
    result = [f"Khách sạn tại {city} (≤ {format_price(max_price_per_night)}/đêm):"]

    for hotel in filtered_hotels:
        result.append(
            f"- {hotel['name']} | {hotel['stars']}⭐ | "
            f"{hotel['area']} | {format_price(hotel['price_per_night'])}/đêm | "
            f"⭐{hotel['rating']}"
        )

    return "\n".join(result)

@tool
def calculate_budget(total_budget: int, expenses: str) -> str:
    """
    Tính toán chi tiết ngân sách du lịch: liệt kê các khoản chi và số tiền còn lại.
    
    Dùng tool này khi cần:
    - Giúp khách hàng theo dõi ngân sách du lịch
    - Hiển thị chi tiết các khoản chi (vé máy bay, khách sạn, ăn uống, mua sắm, v.v.)
    - Cảnh báo nếu chi phí vượt quá ngân sách
    - Tính toán số tiền còn lại cho các hoạt động khác
    
    Lưu ý: Đây là CÔNG CỤ TÍNH TOÁN, không phải để đặt chỗ hay thanh toán. Dùng khi có giá từ tools khác.

    Tham số:
        total_budget: tổng ngân sách ban đầu (VNĐ). Ví dụ: 10_000_000 (10 triệu)
        expenses: các khoản chi phí dưới dạng chuỗi, phân tách bằng dấu phẩy.
                  Định dạng: 'tên_khoản: số_tiền, tên_khoản_khác: số_tiền'
                  Ví dụ: 'vé_máy_bay: 890000, khách_sạn: 1200000, ăn_uống: 500000'
                  
                  Tên khoản phổ biến:
                  - vé_máy_bay: Giá vé máy bay
                  - khách_sạn: Giá phòng (thường nhân với số đêm)
                  - ăn_uống: Chi phí ăn uống
                  - mua_sắm: Chi phí mua sắm/giải trí
                  - giao_thông: Chi phí di chuyển trong thành phố

    Trả về:
        Bảng chi tiết gồm:
        - Danh sách chi tiết từng khoản chi
        - Tổng chi phí (VNĐ)
        - Tổng ngân sách (VNĐ)
        - Số tiền còn lại (nếu >= 0) hoặc cảnh báo VƯỢT NGÂN SÁCH (nếu < 0)
        
        Nếu chi phí vượt quá ngân sách, gợi ý điều chỉnh - giảm chi phí hoặc tăng ngân sách.
    """

    def format_price(price: int) -> str:
        return f"{price:,}".replace(",", ".") + "₫"

    # Parse expenses
    expense_dict = {}
    try:
        items = [item.strip() for item in expenses.split(",") if item.strip()]

        for item in items:
            name, value = item.split(":")
            name = name.strip().replace("_", " ").capitalize()
            value = int(value.strip())
            expense_dict[name] = value

    except Exception:
        return "Lỗi định dạng expenses. Vui lòng dùng dạng: 'vé_máy_bay: 890000, khách_sạn: 650000'"

    # Tính toán
    total_expense = sum(expense_dict.values())
    remaining = total_budget - total_expense

    # Format output
    result = ["Bảng chi phí:"]

    for name, value in expense_dict.items():
        result.append(f"- {name}: {format_price(value)}")

    result.append(f"\nTổng chi: {format_price(total_expense)}")
    result.append(f"Ngân sách: {format_price(total_budget)}")

    if remaining >= 0:
        result.append(f"Còn lại: {format_price(remaining)}")
    else:
        result.append(f"Vượt ngân sách {format_price(abs(remaining))}! Cần điều chỉnh.")

    return "\n".join(result)