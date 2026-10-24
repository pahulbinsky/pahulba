<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Локальный сервер</title>
    <style>
        body {
            margin: 0;
            padding: 20px;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            background-color: #f4f6f9;
        }
        h1 {
            color: #1e293b;
            font-size: 24px;
            margin-bottom: 20px;
            padding-left: 5px;
        }
        .search-input {
            width: 100%;
            max-width: 300px;
            padding: 10px 12px;
            margin-bottom: 20px;
            border: 1px solid #cbd5e1;
            border-radius: 6px;
            font-size: 14px;
            outline: none;
        }
        .search-input:focus {
            border-color: #2563eb;
            box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.2);
        }
        .button-list {
            display: flex;
            flex-direction: column; 
            gap: 10px;              
            max-width: 320px;       
        }
        .folder-link {
            display: flex;
            align-items: center;
            padding: 14px 18px;
            background-color: #ffffff;
            color: #1e293b;
            text-decoration: none;
            border-radius: 8px;
            font-size: 15px;
            font-weight: 500;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
            border: 1px solid #e2e8f0;
            transition: all 0.15s ease-in-out;
        }
        .folder-link:hover {
            background-color: #2563eb;
            border-color: #2563eb;
            color: #ffffff;
            transform: translateX(4px);
        }
        .folder-link::before {
            content: "📁";
            margin-right: 12px;
            font-size: 16px;
        }
    </style>
</head>
<body>

    <h1>Локальный сервер</h1>

    <input type="text" id="searchInput" class="search-input" placeholder="Поиск папки...">

    <div class="button-list">
        <?php
        $dir = __DIR__;
        $items = scandir($dir);

        foreach ($items as $item) {
            if ($item === '.' || $item === '..') {
                continue;
            }

            if (is_dir($dir . '/' . $item)) {
                echo '<a href="' . htmlspecialchars($item) . '/" class="folder-link">' . htmlspecialchars($item) . '</a>' . PHP_EOL;
            }
        }
        ?>
    </div>

    <script>
        document.getElementById('searchInput').addEventListener('input', function() {
            const filter = this.value.toLowerCase();
            const links = document.querySelectorAll('.folder-link');
            
            links.forEach(link => {
                const text = link.textContent.toLowerCase();
                if (text.includes(filter)) {
                    link.style.display = 'flex';
                } else {
                    link.style.display = 'none';
                }
            });
        });
    </script>

</body>
</html>
