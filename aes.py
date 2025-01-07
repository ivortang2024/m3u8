from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from binascii import unhexlify


def aes_decode(hex_str):
    # 密钥和初始向量
    key = b'181cc88340ae5b2b'  # 16 字节密钥 (128 位)
    iv = b'4423d1e2773476ce'  # 16 字节初始向量 (128 位)

    # 将十六进制字符串转换为二进制数据
    encrypted_data = unhexlify(hex_str)

    # 创建 AES 解密器
    cipher = AES.new(key, AES.MODE_CBC, iv)

    # 解密并去除填充
    decrypted_data = unpad(cipher.decrypt(encrypted_data), AES.block_size)

    # 转换为字符串并返回
    return decrypted_data.decode('utf-8')


# 示例
if __name__ == "__main__":
    encrypted_hex = "d9f8c51be8fc3d2018e9a26b8f4c9e3f"  # 替换为实际的加密字符串
    decrypted_text = aes_decode(encrypted_hex)
    print("解密后的明文:", decrypted_text)
