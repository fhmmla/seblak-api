import time

class MahasiswaAlgo:
    # 1. INSERTION SORT (O(n^2))
    @staticmethod
    def insertion_sort(data, key):
        arr = list(data)
        for i in range(1, len(arr)):
            current = arr[i]
            j = i - 1
            while j >= 0 and arr[j][key] > current[key]:
                arr[j + 1] = arr[j]
                j -= 1
            arr[j + 1] = current
        return arr

    # 2. SELECTION SORT (O(n^2))
    @staticmethod
    def selection_sort(data, key):
        arr = list(data)
        n = len(arr)
        for i in range(n):
            min_idx = i
            for j in range(i + 1, n):
                if arr[j][key] < arr[min_idx][key]:
                    min_idx = j
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
        return arr

    # 3. LINEAR SEARCH (O(n)) - Exact match berdasarkan NIM
    @staticmethod
    def linear_search(data, nim):
        for item in data:
            if item["nim"] == nim:
                return item
        return None

    # 4. SEQUENTIAL SEARCH (O(n)) - Partial match berdasarkan keyword di semua field
    @staticmethod
    def sequential_search(data, keyword):
        results = []
        keyword_lower = keyword.lower()
        for item in data:
            # Cek apakah keyword cocok di salah satu field (nama, nim, jurusan, kelas)
            if (keyword_lower in item["nama"].lower() or
                keyword_lower in item["nim"].lower() or
                keyword_lower in item["jurusan"].lower() or
                keyword_lower in item["kelas"].lower()):
                results.append(item)
        return results

    # 5. BINARY SEARCH (O(log n)) - Data harus di-sort dulu
    @staticmethod
    def binary_search(data, nim):
        # Sort dulu berdasarkan nim sebelum binary search
        sorted_data = MahasiswaAlgo.selection_sort(data, "nim")
        low = 0
        high = len(sorted_data) - 1
        
        while low <= high:
            mid = (low + high) // 2
            if sorted_data[mid]["nim"] == nim:
                return sorted_data[mid]
            elif sorted_data[mid]["nim"] < nim:
                low = mid + 1
            else:
                high = mid - 1
        return None