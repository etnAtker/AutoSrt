import os


class SRT:
    def __init__(self):
        self.lines = []
        pass

    def add_line(self, line):
        self.lines.append(line)


class SRTLine:
    def __init__(self):
        pass


def from_file(filename: str | os.PathLike[str], encoding: str = 'utf-8') -> SRT:
    srt = SRT()
    with open(filename, 'r', encoding=encoding) as f:
        ori_lines = f.readlines()
        i = 0
        while True:
            i, srt_line = parse_line(ori_lines, i)
            srt.add_line(srt_line)

            if i >= len(ori_lines):
                break

    return srt


def parse_line(lines: list[str], start: int = 0) -> tuple[int, SRTLine]:
    srt_line = SRTLine()
    i = start

    while len(lines[i].strip()) > 0:
        i += 1

    srt_line.index = lines[i].strip()
    [start_time, end_time] = lines[i + 1].split('-->')
    srt_line.start_time = str_to_ms(start_time)
    srt_line.end_time = str_to_ms(end_time)

    i += 2
    srt_line.content = ''
    while lines[i] == '\n' or len(lines) >= i:
        srt_line.content += lines[i]
        i += 1

    return i + 1, srt_line


def str_to_ms(time: str) -> int:
    time = time.strip()
    h = int(time[0:2])
    m = int(time[3:5])
    s = int(time[6:8])
    ms = int(time[9:])

    return (h * 60 * 60 + m * 60 + s) * 1000 + ms


def ms_to_str(ms: int) -> str:
    h = int(ms / (60 * 60 * 1000))
    ms -= h * 60 * 60 * 1000

    m = int(ms / (60 * 1000))
    ms -= m * 60 * 1000

    s = int(ms / 1000)
    ms -= s * 1000

    return f'{h:02}:{m:02}:{s:02},{ms:03}'
