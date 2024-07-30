# Test vectors taken from Section 5 of draft-irtf-cfrg-kangarootwelve
# https://datatracker.ietf.org/doc/draft-irtf-cfrg-kangarootwelve/
# Formatted into python dictionaries for easier parsing...


def create_pattern(byte_val, length):
    """
    Create test vector patterns
    """
    return bytes([x % (byte_val + 1) for x in range(length)])


def test_create_pattern():
    """
    Check that pattern creation works as documented
    """
    ptn_17 = "00 01 02 03 04 05 06 07 08 09 0A 0B 0C 0D 0E 0F 10".replace(" ", "")
    ptn_17_2 = """00 01 02 03 04 05 06 07 08 09 0A 0B 0C 0D 0E 0F
        10 11 12 13 14 15 16 17 18 19 1A 1B 1C 1D 1E 1F
        20 21 22 23 24 25 26 27 28 29 2A 2B 2C 2D 2E 2F
        30 31 32 33 34 35 36 37 38 39 3A 3B 3C 3D 3E 3F
        40 41 42 43 44 45 46 47 48 49 4A 4B 4C 4D 4E 4F
        50 51 52 53 54 55 56 57 58 59 5A 5B 5C 5D 5E 5F
        60 61 62 63 64 65 66 67 68 69 6A 6B 6C 6D 6E 6F
        70 71 72 73 74 75 76 77 78 79 7A 7B 7C 7D 7E 7F
        80 81 82 83 84 85 86 87 88 89 8A 8B 8C 8D 8E 8F
        90 91 92 93 94 95 96 97 98 99 9A 9B 9C 9D 9E 9F
        A0 A1 A2 A3 A4 A5 A6 A7 A8 A9 AA AB AC AD AE AF
        B0 B1 B2 B3 B4 B5 B6 B7 B8 B9 BA BB BC BD BE BF
        C0 C1 C2 C3 C4 C5 C6 C7 C8 C9 CA CB CC CD CE CF
        D0 D1 D2 D3 D4 D5 D6 D7 D8 D9 DA DB DC DD DE DF
        E0 E1 E2 E3 E4 E5 E6 E7 E8 E9 EA EB EC ED EE EF
        F0 F1 F2 F3 F4 F5 F6 F7 F8 F9 FA
        00 01 02 03 04 05 06 07 08 09 0A 0B 0C 0D 0E 0F
        10 11 12 13 14 15 16 17 18 19 1A 1B 1C 1D 1E 1F
        20 21 22 23 24 25""".replace("\n", "").replace(" ", "")

    assert bytes.fromhex(ptn_17) == create_pattern(0xFA, 17)
    assert bytes.fromhex(ptn_17_2) == create_pattern(0xFA, 17**2)


turbo_shake_128_test_vectors = [
    {
        "msg": b"",
        "out_len": 32,
        "D": 0x07,
        "output_bytes": "5A 22 3A D3 0B 3B 8C 66 A2 43 04 8C FC ED 43 0F 54 E7 52 92 87 D1 51 50 B9 73 13 3A DF AC 6A 2F",
    },
    {
        "msg": b"",
        "out_len": 64,
        "D": 0x07,
        "output_bytes": "5A 22 3A D3 0B 3B 8C 66 A2 43 04 8C FC ED 43 0F 54 E7 52 92 87 D1 51 50 B9 73 13 3A DF AC 6A 2F FE 27 08 E7 30 61 E0 9A 40 00 16 8B A9 C8 CA 18 13 19 8F 7B BE D4 98 4B 41 85 F2 C2 58 0E E6 23",
    },
    {
        "msg": b"",
        "out_len": 10032,
        "D": 0x07,
        "last": 32,
        "output_bytes": "75 93 A2 80 20 A3 C4 AE 0D 60 5F D6 1F 5E B5 6E CC D2 7C C3 D1 2F F0 9F 78 36 97 72 A4 60 C5 5D",
    },
    {
        "msg": create_pattern(0xFA, 1),
        "out_len": 32,
        "D": 0x07,
        "output_bytes": "1A C2 D4 50 FC 3B 42 05 D1 9D A7 BF CA 1B 37 51 3C 08 03 57 7A C7 16 7F 06 FE 2C E1 F0 EF 39 E5",
    },
    {
        "msg": create_pattern(0xFA, 17),
        "out_len": 32,
        "D": 0x07,
        "output_bytes": "AC BD 4A A5 75 07 04 3B CE E5 5A D3 F4 85 04 D8 15 E7 07 FE 82 EE 3D AD 6D 58 52 C8 92 0B 90 5E",
    },
    {
        "msg": create_pattern(0xFA, 17**2),
        "out_len": 32,
        "D": 0x07,
        "output_bytes": "7A 4D E8 B1 D9 27 A6 82 B9 29 61 01 03 F0 E9 64 55 9B D7 45 42 CF AD 74 0E E3 D9 B0 36 46 9E 0A",
    },
    {
        "msg": create_pattern(0xFA, 17**3),
        "out_len": 32,
        "D": 0x07,
        "output_bytes": "74 52 ED 0E D8 60 AA 8F E8 E7 96 99 EC E3 24 F8 D9 32 71 46 36 10 DA 76 80 1E BC EE 4F CA FE 42",
    },
    {
        "msg": create_pattern(0xFA, 17**4),
        "out_len": 32,
        "D": 0x07,
        "output_bytes": "CA 5F 1F 3E EA C9 92 CD C2 AB EB CA 0E 21 67 65 DB F7 79 C3 C1 09 46 05 5A 94 AB 32 72 57 35 22",
    },
    {
        "msg": create_pattern(0xFA, 17**5),
        "out_len": 32,
        "D": 0x07,
        "output_bytes": "E9 88 19 3F B9 11 9F 11 CD 34 46 79 14 E2 A2 6D A9 BD F9 6C 8B EF 07 6A EE AD 1A 89 7B 86 63 83",
    },
    {
        "msg": create_pattern(0xFA, 17**6),
        "out_len": 32,
        "D": 0x07,
        "output_bytes": "9C 0F FB 98 7E EE ED AD FA 55 94 89 87 75 6D 09 0B 67 CC B6 12 36 E3 06 AC 8A 24 DE 1D 0A F7 74",
    },
    {
        "msg": b"",
        "out_len": 32,
        "D": 0x0B,
        "output_bytes": "8B 03 5A B8 F8 EA 7B 41 02 17 16 74 58 33 2E 46 F5 4B E4 FF 83 54 BA F3 68 71 04 A6 D2 4B 0E AB",
    },
    {
        "msg": b"",
        "out_len": 32,
        "D": 0x06,
        "output_bytes": "C7 90 29 30 6B FA 2F 17 83 6A 3D 65 16 D5 56 63 40 FE A6 EB 1A 11 39 AD 90 0B 41 24 3C 49 4B 37",
    },
    {
        "msg": bytes.fromhex("FF"),
        "out_len": 32,
        "D": 0x06,
        "output_bytes": "8E C9 C6 64 65 ED 0D 4A 6C 35 D1 35 06 71 8D 68 7A 25 CB 05 C7 4C CA 1E 42 50 1A BD 83 87 4A 67",
    },
    {
        "msg": bytes.fromhex("FFFFFF"),
        "out_len": 32,
        "D": 0x06,
        "output_bytes": "3D 03 98 8B B5 9E 68 18 51 A1 92 F4 29 AE 03 98 8E 8F 44 4B C0 60 36 A3 F1 A7 D2 CC D7 58 D1 74",
    },
    {
        "msg": bytes.fromhex("FFFFFFFFFFFFFF"),
        "out_len": 32,
        "D": 0x06,
        "output_bytes": "05 D9 AE 67 3D 5F 0E 48 BB 2B 57 E8 80 21 A1 A8 3D 70 BA 85 92 3A A0 4C 12 E8 F6 5B A1 F9 45 95",
    },
    {
        "msg": b"",
        "out_len": 32,
        "D": 0x1F,
        "output_bytes": "1E 41 5F 1C 59 83 AF F2 16 92 17 27 7D 17 BB 53 8C D9 45 A3 97 DD EC 54 1F 1C E4 1A F2 C1 B7 4C",
    },
    {
        "msg": b"",
        "out_len": 64,
        "D": 0x1F,
        "output_bytes": "1E 41 5F 1C 59 83 AF F2 16 92 17 27 7D 17 BB 53 8C D9 45 A3 97 DD EC 54 1F 1C E4 1A F2 C1 B7 4C 3E 8C CA E2 A4 DA E5 6C 84 A0 4C 23 85 C0 3C 15 E8 19 3B DF 58 73 73 63 32 16 91 C0 54 62 C8 DF",
    },
    {
        "msg": b"",
        "out_len": 10032,
        "D": 0x1F,
        "last": 32,
        "output_bytes": "A3 B9 B0 38 59 00 CE 76 1F 22 AE D5 48 E7 54 DA 10 A5 24 2D 62 E8 C6 58 E3 F3 A9 23 A7 55 56 07",
    },
    {
        "msg": create_pattern(0xFA, 17**0),
        "out_len": 32,
        "D": 0x1F,
        "output_bytes": "55 CE DD 6F 60 AF 7B B2 9A 40 42 AE 83 2E F3 F5 8D B7 29 9F 89 3E BB 92 47 24 7D 85 69 58 DA A9",
    },
    {
        "msg": create_pattern(0xFA, 17**1),
        "out_len": 32,
        "D": 0x1F,
        "output_bytes": "9C 97 D0 36 A3 BA C8 19 DB 70 ED E0 CA 55 4E C6 E4 C2 A1 A4 FF BF D9 EC 26 9C A6 A1 11 16 12 33",
    },
    {
        "msg": create_pattern(0xFA, 17**2),
        "out_len": 32,
        "D": 0x1F,
        "output_bytes": "96 C7 7C 27 9E 01 26 F7 FC 07 C9 B0 7F 5C DA E1 E0 BE 60 BD BE 10 62 00 40 E7 5D 72 23 A6 24 D2",
    },
    {
        "msg": create_pattern(0xFA, 17**3),
        "out_len": 32,
        "D": 0x1F,
        "output_bytes": "D4 97 6E B5 6B CF 11 85 20 58 2B 70 9F 73 E1 D6 85 3E 00 1F DA F8 0E 1B 13 E0 D0 59 9D 5F B3 72",
    },
    {
        "msg": create_pattern(0xFA, 17**4),
        "out_len": 32,
        "D": 0x1F,
        "output_bytes": "DA 67 C7 03 9E 98 BF 53 0C F7 A3 78 30 C6 66 4E 14 CB AB 7F 54 0F 58 40 3B 1B 82 95 13 18 EE 5C",
    },
    {
        "msg": create_pattern(0xFA, 17**5),
        "out_len": 32,
        "D": 0x1F,
        "output_bytes": "B9 7A 90 6F BF 83 EF 7C 81 25 17 AB F3 B2 D0 AE A0 C4 F6 03 18 CE 11 CF 10 39 25 12 7F 59 EE CD",
    },
    {
        "msg": create_pattern(0xFA, 17**6),
        "out_len": 32,
        "D": 0x1F,
        "output_bytes": "35 CD 49 4A DE DE D2 F2 52 39 AF 09 A7 B8 EF 0C 4D 1C A4 FE 2D 1A C3 70 FA 63 21 6F E7 B4 C2 B1",
    },
    {
        "msg": bytes.fromhex("FFFFFF"),
        "out_len": 32,
        "D": 0x01,
        "output_bytes": "BF 32 3F 94 04 94 E8 8E E1 C5 40 FE 66 0B E8 A0 C9 3F 43 D1 5E C0 06 99 84 62 FA 99 4E ED 5D AB",
    },
    {
        "msg": bytes.fromhex("FF"),
        "out_len": 32,
        "D": 0x06,
        "output_bytes": "8E C9 C6 64 65 ED 0D 4A 6C 35 D1 35 06 71 8D 68 7A 25 CB 05 C7 4C CA 1E 42 50 1A BD 83 87 4A 67",
    },
    {
        "msg": bytes.fromhex("FFFFFF"),
        "out_len": 32,
        "D": 0x07,
        "output_bytes": "B6 58 57 60 01 CA D9 B1 E5 F3 99 A9 F7 77 23 BB A0 54 58 04 2D 68 20 6F 72 52 68 2D BA 36 63 ED",
    },
    {
        "msg": bytes.fromhex("FFFFFFFFFFFFFF"),
        "out_len": 32,
        "D": 0x0B,
        "output_bytes": "8D EE AA 1A EC 47 CC EE 56 9F 65 9C 21 DF A8 E1 12 DB 3C EE 37 B1 81 78 B2 AC D8 05 B7 99 CC 37",
    },
    {
        "msg": bytes.fromhex("FF"),
        "out_len": 32,
        "D": 0x30,
        "output_bytes": "55 31 22 E2 13 5E 36 3C 32 92 BE D2 C6 42 1F A2 32 BA B0 3D AA 07 C7 D6 63 66 03 28 65 06 32 5B",
    },
    {
        "msg": bytes.fromhex("FFFFFF"),
        "out_len": 32,
        "D": 0x7F,
        "output_bytes": "16 27 4C C6 56 D4 4C EF D4 22 39 5D 0F 90 53 BD A6 D2 8E 12 2A BA 15 C7 65 E5 AD 0E 6E AF 26 F9",
    },
]

turbo_shake_256_test_vectors = [
    {
        "msg": b"",
        "out_len": 64,
        "D": 0x07,
        "output_bytes": "4A 55 5B 06 EC F8 F1 53 8C CF 5C 95 15 D0 D0 49 70 18 15 63 A6 23 81 C7 F0 C8 07 A6 D1 BD 9E 81 97 80 4B FD E2 42 8B F7 29 61 EB 52 B4 18 9C 39 1C EF 6F EE 66 3A 3C 1C E7 8B 88 25 5B C1 AC C3",
    },
    {
        "msg": b"",
        "out_len": 10032,
        "last": 32,
        "D": 0x07,
        "output_bytes": "40 22 1A D7 34 F3 ED C1 B1 06 BA D5 0A 72 94 93 15 B3 52 BA 39 AD 98 B5 B3 C2 30 11 63 AD AA D0",
    },
    {
        "msg": create_pattern(0xFA, 17),
        "out_len": 64,
        "D": 0x07,
        "output_bytes": "66 D3 78 DF E4 E9 02 AC 4E B7 8F 7C 2E 5A 14 F0 2B C1 C8 49 E6 21 BA E6 65 79 6F B3 34 6E 6C 79 75 70 5B B9 3C 00 F3 CA 8F 83 BC A4 79 F0 69 77 AB 3A 60 F3 97 96 B1 36 53 8A AA E8 BC AC 85 44",
    },
    {
        "msg": create_pattern(0xFA, 17**2),
        "out_len": 64,
        "D": 0x07,
        "output_bytes": "C5 21 74 AB F2 82 95 E1 5D FB 37 B9 46 AC 36 BD 3A 6B CC 98 C0 74 FC 25 19 9E 05 30 42 5C C5 ED D4 DF D4 3D C3 E7 E6 49 1A 13 17 98 30 C3 C7 50 C9 23 7E 83 FD 9A 3F EC 46 03 FF 57 E4 22 2E F2",
    },
    {
        "msg": create_pattern(0xFA, 17**3),
        "out_len": 64,
        "D": 0x07,
        "output_bytes": "62 A5 A0 BF F0 64 26 D7 1A 7A 3E 9E 3F 2F D6 E2 52 FF 3F C1 88 A6 A5 36 EC A4 5A 49 A3 43 7C B3 BC 3A 0F 81 49 C8 50 E6 E7 F4 74 7A 70 62 7F D2 30 30 41 C6 C3 36 30 F9 43 AD 92 F8 E1 FF 43 90",
    },
    {
        "msg": create_pattern(0xFA, 17**4),
        "out_len": 64,
        "D": 0x07,
        "output_bytes": "52 3C 06 47 18 2D 89 41 F0 DD 5C 5C 0A B6 2D 4F C2 95 61 61 53 96 BB 5B 9A 9D EB 02 2B 80 C5 BF 2D 83 A3 BB 36 FF C0 4F AC 58 CF 11 49 C6 6D EC 4A 59 52 6E 51 F2 95 96 D8 24 42 1A 4B 84 B4 4D",
    },
    {
        "msg": create_pattern(0xFA, 17**5),
        "out_len": 64,
        "D": 0x07,
        "output_bytes": "D1 14 A1 C1 A2 08 FF 05 FD 49 D0 9E E0 35 46 5D 86 54 7E BA D8 E9 AF 4F 8E 87 53 70 57 3D 6B 7B B2 0A B9 60 63 5A B5 74 E2 21 95 EF 9D 17 1C 9A 28 01 04 4B 6E 2E DF 27 2E 23 02 55 4B 3A 77 C9",
    },
    {
        "msg": create_pattern(0xFA, 17**6),
        "out_len": 64,
        "D": 0x07,
        "output_bytes": "1E 51 34 95 D6 16 98 75 B5 94 53 A5 94 E0 8A E2 71 CA 20 E0 56 43 C8 8A 98 7B 5B 6A B4 23 ED E7 24 0F 34 F2 B3 35 FA 94 BC 4B 0D 70 E3 1F B6 33 B0 79 84 43 31 FE A4 2A 9C 4D 79 BB 8C 5F 9E 73",
    },
    {
        "msg": b"",
        "out_len": 64,
        "D": 0x0B,
        "output_bytes": "C7 49 F7 FB 23 64 4A 02 1D 35 65 3D 1B FD F7 47 CE CE 5F 97 39 F9 A3 44 AD 16 9F 10 90 6C 68 17 C8 EE 12 78 4E 42 FF 57 81 4E FC 1C 89 87 89 D5 E4 15 DB 49 05 2E A4 3A 09 90 1D 7A 82 A2 14 5C",
    },
    {
        "msg": b"",
        "out_len": 64,
        "D": 0x06,
        "output_bytes": "FF 23 DC CD 62 16 8F 5A 44 46 52 49 A8 6D C1 0E 8A AB 4B D2 6A 22 DE BF 23 48 02 0A 83 1C DB E1 2C DD 36 A7 DD D3 1E 71 C0 1F 7C 97 A0 D4 C3 A0 CC 1B 21 21 E6 B7 CE AB 38 87 A4 C9 A5 AF 8B 03",
    },
    {
        "msg": bytes.fromhex("FF"),
        "out_len": 64,
        "D": 0x06,
        "output_bytes": "73 8D 7B 4E 37 D1 8B 7F 22 AD 1B 53 13 E3 57 E3 DD 7D 07 05 6A 26 A3 03 C4 33 FA 35 33 45 52 80 F4 F5 A7 D4 F7 00 EF B4 37 FE 6D 28 14 05 E0 7B E3 2A 0A 97 2E 22 E6 3A DC 1B 09 0D AE FE 00 4B",
    },
    {
        "msg": bytes.fromhex("FF FF FF"),
        "out_len": 64,
        "D": 0x06,
        "output_bytes": "E5 53 8C DD 28 30 2A 2E 81 E4 1F 65 FD 2A 40 52 01 4D 0C D4 63 DF 67 1D 1E 51 0A 9D 95 C3 7D 71 35 EF 27 28 43 0A 9E 31 70 04 F8 36 C9 A2 38 EF 35 37 02 80 D0 3D CE 7F 06 12 F0 31 5B 3C BF 63",
    },
    {
        "msg": bytes.fromhex("FF FF FF FF FF FF FF"),
        "out_len": 64,
        "D": 0x06,
        "output_bytes": "B3 8B 8C 15 F4 A6 E8 0C D3 EC 64 5F 99 9F 64 98 AA D7 A5 9A 48 9C 1D EE 29 70 8B 4F 8A 59 E1 24 99 A9 6F 89 37 22 56 FE 52 2B 1B 97 47 2A DD 73 69 15 BD 4D F9 3B 21 FF E5 97 21 7E B3 C2 C6 D9",
    },
    {
        "msg": b"",
        "out_len": 64,
        "D": 0x1F,
        "output_bytes": "36 7A 32 9D AF EA 87 1C 78 02 EC 67 F9 05 AE 13 C5 76 95 DC 2C 66 63 C6 10 35 F5 9A 18 F8 E7 DB 11 ED C0 E1 2E 91 EA 60 EB 6B 32 DF 06 DD 7F 00 2F BA FA BB 6E 13 EC 1C C2 0D 99 55 47 60 0D B0",
    },
    {
        "msg": b"",
        "out_len": 10032,
        "D": 0x1F,
        "last": 32,
        "output_bytes": "AB EF A1 16 30 C6 61 26 92 49 74 26 85 EC 08 2F 20 72 65 DC CF 2F 43 53 4E 9C 61 BA 0C 9D 1D 75",
    },
    {
        "msg": create_pattern(0xFA, 17**0),
        "out_len": 64,
        "D": 0x1F,
        "output_bytes": "3E 17 12 F9 28 F8 EA F1 05 46 32 B2 AA 0A 24 6E D8 B0 C3 78 72 8F 60 BC 97 04 10 15 5C 28 82 0E 90 CC 90 D8 A3 00 6A A2 37 2C 5C 5E A1 76 B0 68 2B F2 2B AE 74 67 AC 94 F7 4D 43 D3 9B 04 82 E2",
    },
    {
        "msg": create_pattern(0xFA, 17**1),
        "out_len": 64,
        "D": 0x1F,
        "output_bytes": "B3 BA B0 30 0E 6A 19 1F BE 61 37 93 98 35 92 35 78 79 4E A5 48 43 F5 01 10 90 FA 2F 37 80 A9 E5 CB 22 C5 9D 78 B4 0A 0F BF F9 E6 72 C0 FB E0 97 0B D2 C8 45 09 1C 60 44 D6 87 05 4D A5 D8 E9 C7",
    },
    {
        "msg": create_pattern(0xFA, 17**2),
        "out_len": 64,
        "D": 0x1F,
        "output_bytes": "66 B8 10 DB 8E 90 78 04 24 C0 84 73 72 FD C9 57 10 88 2F DE 31 C6 DF 75 BE B9 D4 CD 93 05 CF CA E3 5E 7B 83 E8 B7 E6 EB 4B 78 60 58 80 11 63 16 FE 2C 07 8A 09 B9 4A D7 B8 21 3C 0A 73 8B 65 C0",
    },
    {
        "msg": create_pattern(0xFA, 17**3),
        "out_len": 64,
        "D": 0x1F,
        "output_bytes": "C7 4E BC 91 9A 5B 3B 0D D1 22 81 85 BA 02 D2 9E F4 42 D6 9D 3D 42 76 A9 3E FE 0B F9 A1 6A 7D C0 CD 4E AB AD AB 8C D7 A5 ED D9 66 95 F5 D3 60 AB E0 9E 2C 65 11 A3 EC 39 7D A3 B7 6B 9E 16 74 FB",
    },
    {
        "msg": create_pattern(0xFA, 17**4),
        "out_len": 64,
        "D": 0x1F,
        "output_bytes": "02 CC 3A 88 97 E6 F4 F6 CC B6 FD 46 63 1B 1F 52 07 B6 6C 6D E9 C7 B5 5B 2D 1A 23 13 4A 17 0A FD AC 23 4E AB A9 A7 7C FF 88 C1 F0 20 B7 37 24 61 8C 56 87 B3 62 C4 30 B2 48 CD 38 64 7F 84 8A 1D",
    },
    {
        "msg": create_pattern(0xFA, 17**5),
        "out_len": 64,
        "D": 0x1F,
        "output_bytes": "AD D5 3B 06 54 3E 58 4B 58 23 F6 26 99 6A EE 50 FE 45 ED 15 F2 02 43 A7 16 54 85 AC B4 AA 76 B4 FF DA 75 CE DF 6D 8C DC 95 C3 32 BD 56 F4 B9 86 B5 8B B1 7D 17 78 BF C1 B1 A9 75 45 CD F4 EC 9F",
    },
    {
        "msg": create_pattern(0xFA, 17**6),
        "out_len": 64,
        "D": 0x1F,
        "output_bytes": "9E 11 BC 59 C2 4E 73 99 3C 14 84 EC 66 35 8E F7 1D B7 4A EF D8 4E 12 3F 78 00 BA 9C 48 53 E0 2C FE 70 1D 9E 6B B7 65 A3 04 F0 DC 34 A4 EE 3B A8 2C 41 0F 0D A7 0E 86 BF BD 90 EA 87 7C 2D 61 04",
    },
    {
        "msg": bytes.fromhex("FFFFFF"),
        "out_len": 64,
        "D": 0x01,
        "output_bytes": "D2 1C 6F BB F5 87 FA 22 82 F2 9A EA 62 01 75 FB 02 57 41 3A F7 8A 0B 1B 2A 87 41 9C E0 31 D9 33 AE 7A 4D 38 33 27 A8 A1 76 41 A3 4F 8A 1D 10 03 AD 7D A6 B7 2D BA 84 BB 62 FE F2 8F 62 F1 24 24",
    },
    {
        "msg": bytes.fromhex("FF"),
        "out_len": 64,
        "D": 0x06,
        "output_bytes": "73 8D 7B 4E 37 D1 8B 7F 22 AD 1B 53 13 E3 57 E3 DD 7D 07 05 6A 26 A3 03 C4 33 FA 35 33 45 52 80 F4 F5 A7 D4 F7 00 EF B4 37 FE 6D 28 14 05 E0 7B E3 2A 0A 97 2E 22 E6 3A DC 1B 09 0D AE FE 00 4B",
    },
    {
        "msg": bytes.fromhex("FFFFFF"),
        "out_len": 64,
        "D": 0x07,
        "output_bytes": "18 B3 B5 B7 06 1C 2E 67 C1 75 3A 00 E6 AD 7E D7 BA 1C 90 6C F9 3E FB 70 92 EA F2 7F BE EB B7 55 AE 6E 29 24 93 C1 10 E4 8D 26 00 28 49 2B 8E 09 B5 50 06 12 B8 F2 57 89 85 DE D5 35 7D 00 EC 67",
    },
    {
        "msg": bytes.fromhex("FFFFFFFFFFFFFF"),
        "out_len": 64,
        "D": 0x0B,
        "output_bytes": "BB 36 76 49 51 EC 97 E9 D8 5F 7E E9 A6 7A 77 18 FC 00 5C F4 25 56 BE 79 CE 12 C0 BD E5 0E 57 36 D6 63 2B 0D 0D FB 20 2D 1B BB 8F FE 3D D7 4C B0 08 34 FA 75 6C B0 34 71 BA B1 3A 1E 2C 16 B3 C0",
    },
    {
        "msg": bytes.fromhex("FF"),
        "out_len": 64,
        "D": 0x30,
        "output_bytes": "F3 FE 12 87 3D 34 BC BB 2E 60 87 79 D6 B7 0E 7F 86 BE C7 E9 0B F1 13 CB D4 FD D0 C4 E2 F4 62 5E 14 8D D7 EE 1A 52 77 6C F7 7F 24 05 14 D9 CC FC 3B 5D DA B8 EE 25 5E 39 EE 38 90 72 96 2C 11 1A",
    },
    {
        "msg": bytes.fromhex("FFFFFF"),
        "out_len": 64,
        "D": 0x7F,
        "output_bytes": "AB E5 69 C1 F7 7E C3 40 F0 27 05 E7 D3 7C 9A B7 E1 55 51 6E 4A 6A 15 00 21 D7 0B 6F AC 0B B4 0C 06 9F 9A 98 28 A0 D5 75 CD 99 F9 BA E4 35 AB 1A CF 7E D9 11 0B A9 7C E0 38 8D 07 4B AC 76 87 76",
    },
]
