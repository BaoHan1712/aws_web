from flask import Flask, render_template, jsonify, request
import uuid
import json
import os

app = Flask(__name__)

# --- MOCK DATABASE ---
# Trong thực tế, với dự án production, anh sẽ thay thế phần này bằng SQLAlchemy kết nối với PostgreSQL/MySQL.
PRODUCTS = [
    { "id": 1, "name": "Váy Công Chúa Hồng", "category": "Quần áo", "price": 150000, "img": "https://yunie.com.vn/wp-content/uploads/2023/10/So-vintage-Vang-2-1.jpg" },
    { "id": 2, "name": "Pate Whiskas Vị Cá Thu", "category": "Thức ăn", "price": 25000, "img": "https://images.unsplash.com/photo-1583337130417-3346a1be7dee?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=60" },
    { "id": 3, "name": "Nệm Giường Hình Chân Mèo", "category": "Chuồng nệm", "price": 320000, "img": "https://noithattre24h.com/wp-content/uploads/2022/03/1-35-12.jpg" },
    { "id": 4, "name": "Cần Câu Mèo Gắn Lông Vũ", "category": "Đồ chơi", "price": 45000, "img": "https://images.unsplash.com/photo-1545249390-6bdfa286032f?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=60" },
    { "id": 5, "name": "Vòng Cổ Chuông Pastel", "category": "Phụ kiện", "price": 55000, "img": "https://images.unsplash.com/photo-1576201836106-db1758fd1c97?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=60" },
    { "id": 6, "name": "Bánh Thưởng Cho Cún", "category": "Thức ăn", "price": 65000, "img": "https://thuyhoangbachquan12.com/upload/product/273993237259.jpg" },
    { "id": 7, "name": "Balo Vận Chuyển Trong Suốt", "category": "Phụ kiện", "price": 450000, "img": "https://images.unsplash.com/photo-1596492784531-6e6eb5ea9993?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=60" },
    { "id": 8, "name": "Xương Gặm Sạch Răng", "category": "Đồ chơi", "price": 35000, "img": "https://images.unsplash.com/photo-1623387641168-d9803ddd3f35?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=60" }
]

CATEGORIES = [
    {"id": "food", "name": "Thức ăn", "icon": "🦴", "color": "rose"},
    {"id": "toys", "name": "Đồ chơi", "icon": "🧶", "color": "purple"},
    {"id": "clothes", "name": "Quần áo", "icon": "👗", "color": "blue"},
    {"id": "beds", "name": "Chuồng, nệm", "icon": "🛏️", "color": "yellow"}
]

# --- ROUTES ---

@app.route('/')
def index():
    """
    Route chính render giao diện HTML.
    Truyền dữ liệu từ Backend xuống Frontend bằng Jinja2 context.
    """
    products_json = json.dumps(PRODUCTS)
    return render_template('index.html', categories=CATEGORIES, products=PRODUCTS, products_json=products_json)

# --- API ENDPOINTS (Dành cho xử lý AJAX / Fetch API từ Frontend) ---

@app.route('/api/products', methods=['GET'])
def get_products():
    """API trả về danh sách sản phẩm dưới dạng JSON."""
    # Anh có thể thêm params phân trang (pagination) ở đây: request.args.get('page')
    return jsonify({
        "status": "success",
        "total": len(PRODUCTS),
        "data": PRODUCTS
    })

@app.route('/api/checkout', methods=['POST'])
def checkout():
    """API xử lý thanh toán giỏ hàng."""
    data = request.json
    cart = data.get('cart', [])
    
    if not cart:
        return jsonify({"status": "error", "message": "Giỏ hàng trống"}), 400
        
    # Xử lý logic nghiệp vụ: Kiểm tra tồn kho, tính tổng tiền, lưu database (Bỏ qua bước này ở mock)
    total_amount = sum(item['price'] * item['quantity'] for item in cart)
    
    # Sinh mã đơn hàng ngẫu nhiên (hoặc dùng auto-increment trong DB)
    order_id = f"ORD-{uuid.uuid4().hex[:6].upper()}"
    
    return jsonify({
        "status": "success",
        "message": "Đặt hàng thành công!",
        "order_id": order_id,
        "total": total_amount
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)