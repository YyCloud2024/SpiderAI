// 自定义加密函数
function BloodSpider_encrypt(text, secretKey = "defaultKey") {
    try {
        if (!text) return "";

        // 1. 将文本转换为 UTF-8 编码的字节数组
        const encoder = new TextEncoder();
        let bytes = encoder.encode(text);

        // 2. 使用密钥生成一个伪随机数序列
        const keyBytes = encoder.encode(secretKey);
        const keyLength = keyBytes.length;

        // 3. 对每个字节进行处理：位移 + 异或 + 替换
        for (let i = 0; i < bytes.length; i++) {
            // 基于位置和密钥的复杂变换
            const keyByte = keyBytes[i % keyLength];
            const shift = (keyByte % 7) + 1; // 1-7 的位移量

            // 位移操作
            let newByte = (bytes[i] << shift) | (bytes[i] >>> (8 - shift));

            // 异或操作
            newByte = newByte ^ keyByte;

            // 替换操作（简单的替换表）
            newByte = ((newByte * 17) + 31) % 256;

            bytes[i] = newByte;
        }

        // 4. 将处理后的字节数组转换为 Base64 以便于存储和传输
        // 使用 URL 安全的 Base64 编码，替换 + 和 / 并移除 =
        let base64 = btoa(String.fromCharCode(...bytes))
           .replace(/\+/g, '-')
           .replace(/\//g, '_')
           .replace(/=+$/, '');

        // 5. 添加一些混淆字符，使加密结果更复杂
        const hxzf = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789BloodSpider";
        let result = "";
        for (let i = 0; i < base64.length; i++) {
            const char = base64[i];
            const hxzf_index = (keyBytes[i % keyLength] + i) % hxzf.length;
            result += char + hxzf[hxzf_index];
        }

        return result;
    } catch (e) {
        console.error("加密失败:", e);
        return null;
    }
}

// 自定义解密函数
function BloodSpider_decrypt(encryptedText, secretKey = "defaultKey") {
    try {
        if (!encryptedText) return "";

        // 1. 移除混淆字符
        let base64 = "";
        for (let i = 0; i < encryptedText.length; i += 2) {
            base64 += encryptedText[i];
        }

        // 2. 恢复 Base64 编码
        // 补全缺失的 = 符号
        while (base64.length % 4 !== 0) {
            base64 += '=';
        }
        // 恢复 + 和 /
        base64 = base64.replace(/-/g, '+').replace(/_/g, '/');

        // 3. 解码 Base64 为字节数组
        const binaryString = atob(base64);
        const bytes = new Uint8Array(binaryString.length);
        for (let i = 0; i < binaryString.length; i++) {
            bytes[i] = binaryString.charCodeAt(i);
        }

        // 4. 使用密钥生成伪随机数序列（与加密过程相同）
        const encoder = new TextEncoder();
        const keyBytes = encoder.encode(secretKey);
        const keyLength = keyBytes.length;

        // 5. 逆向处理每个字节：逆替换 + 逆异或 + 逆位移
        for (let i = 0; i < bytes.length; i++) {
            const keyByte = keyBytes[i % keyLength];

            // 逆替换操作
            let newByte = bytes[i];
            // 寻找满足 ((x * 17) + 31) % 256 == newByte 的 x
            let found = false;
            for (let x = 0; x < 256; x++) {
                if (((x * 17) + 31) % 256 === newByte) {
                    newByte = x;
                    found = true;
                    break;
                }
            }
            if (!found) {
                throw new Error("逆替换操作失败");
            }

            // 逆异或操作
            newByte = newByte ^ keyByte;

            // 逆位移操作
            const shift = (keyByte % 7) + 1;
            newByte = (newByte >>> shift) | (newByte << (8 - shift)) & 0xFF;

            bytes[i] = newByte;
        }

        // 6. 将字节数组转换回文本
        const decoder = new TextDecoder();
        return decoder.decode(bytes);
    } catch (e) {
        console.error("解密失败:", e);
        return null;
    }
}

window.BloodSpider_encrypt = BloodSpider_encrypt;
window.BloodSpider_decrypt = BloodSpider_decrypt;

