"""YouTube 영상을 최고 화질(오디오 포함)로 다운로드하는 CLI 앱.

필수 패키지:
	pip install -U yt-dlp
"""

import shutil
import subprocess
from pathlib import Path


def has_audio_stream(file_path: Path) -> bool | None:
	"""ffprobe로 오디오 스트림 존재 여부를 확인한다.

	반환값:
		True: 오디오 스트림 있음
		False: 오디오 스트림 없음
		None: ffprobe 미설치 또는 확인 실패
	"""
	if shutil.which("ffprobe") is None:
		return None

	cmd = [
		"ffprobe",
		"-v",
		"error",
		"-select_streams",
		"a",
		"-show_entries",
		"stream=index",
		"-of",
		"csv=p=0",
		str(file_path),
	]

	try:
		result = subprocess.run(cmd, capture_output=True, text=True, check=False)
		if result.returncode != 0:
			return None
		return bool(result.stdout.strip())
	except Exception:
		return None


def download_youtube_video(url: str, output_dir: Path) -> None:
	"""입력받은 URL의 영상을 최고 화질 + 오디오 포함으로 저장한다."""
	try:
		import yt_dlp  # 지연 import: 패키지 미설치 시 사용자에게 명확히 안내
	except ImportError:
		print("필수 패키지 'yt-dlp'가 설치되어 있지 않습니다.")
		print("다음 명령어로 설치 후 다시 실행하세요: pip install -U yt-dlp")
		return

	output_dir.mkdir(parents=True, exist_ok=True)
	has_ffmpeg = shutil.which("ffmpeg") is not None

	if has_ffmpeg:
		# ffmpeg가 있으면 최고 화질 비디오+오디오를 받아 mp4로 재인코딩한다.
		# 일부 플레이어에서 오디오 코덱 호환성 문제로 무음이 되는 현상을 방지한다.
		format_selector = "bv*+ba/b"
		ffmpeg_options = {
			"merge_output_format": "mp4",
			"recodevideo": "mp4",
			"prefer_ffmpeg": True,
			"postprocessor_args": ["-c:a", "aac", "-b:a", "192k"],
		}
	else:
		# ffmpeg가 없으면 오디오가 포함된 단일 파일 중 최고 화질을 받는다.
		format_selector = "best[acodec!=none][vcodec!=none]/best"
		ffmpeg_options = {}
		print("ffmpeg를 찾을 수 없어 오디오 포함 단일 스트림으로 다운로드합니다.")
		print("분리 스트림 최고 화질 병합을 원하면 ffmpeg를 설치하세요. (brew install ffmpeg)")

	options = {
		"format": format_selector,
		"outtmpl": str(output_dir / "%(title)s.%(ext)s"),
		"noplaylist": True,
		"quiet": False,
		**ffmpeg_options,
	}

	try:
		with yt_dlp.YoutubeDL(options) as ydl:
			info = ydl.extract_info(url, download=True)
			downloaded_path = Path(ydl.prepare_filename(info))

		# recode/merge 후 확장자가 바뀔 수 있어 mp4 결과 파일을 우선 확인한다.
		final_path = downloaded_path
		mp4_path = downloaded_path.with_suffix(".mp4")
		if mp4_path.exists():
			final_path = mp4_path

		print(f"\n다운로드 완료: {final_path.resolve()}")

		audio_ok = has_audio_stream(final_path)
		if audio_ok is True:
			print("오디오 트랙 확인 완료: 소리가 포함되어 있습니다.")
		elif audio_ok is False:
			print("경고: 오디오 트랙이 확인되지 않았습니다. 다른 URL로 다시 시도해 주세요.")
		else:
			print("오디오 트랙 자동 검증을 건너뛰었습니다. (ffprobe 미설치 또는 확인 실패)")
	except Exception as error:
		print(f"다운로드 중 오류가 발생했습니다: {error}")


def main() -> None:
	print("YouTube 다운로드 앱 (최고 화질 + 오디오 포함)")
	url = input("YouTube 영상 주소를 입력하세요: ").strip()

	if not url:
		print("유효한 주소를 입력해야 합니다.")
		return

	if "youtube.com" not in url and "youtu.be" not in url:
		print("YouTube 주소 형식이 아닙니다. 다시 확인해 주세요.")
		return

	download_path = Path("downloads")
	download_youtube_video(url, download_path)


if __name__ == "__main__":
	main()