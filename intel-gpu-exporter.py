from prometheus_client import start_http_server, Gauge
import os
import sys
import subprocess
import json
import logging

igpu_engines_blitter_busy = Gauge(
    "igpu_engines_blitter_busy", "Blitter busy utilisation %"
)
igpu_engines_blitter_sema = Gauge(
    "igpu_engines_blitter_sema", "Blitter sema utilisation %"
)
igpu_engines_blitter_wait = Gauge(
    "igpu_engines_blitter_wait", "Blitter wait utilisation %"
)

igpu_engines_render_3d_busy = Gauge(
    "igpu_engines_render_3d_busy", "Render 3D busy utilisation %"
)
igpu_engines_render_3d_sema = Gauge(
    "igpu_engines_render_3d_sema", "Render 3D sema utilisation %"
)
igpu_engines_render_3d_wait = Gauge(
    "igpu_engines_render_3d_wait", "Render 3D wait utilisation %"
)

igpu_engines_video_busy = Gauge(
    "igpu_engines_video_busy", "Video busy utilisation %"
)
igpu_engines_video_sema = Gauge(
    "igpu_engines_video_sema", "Video sema utilisation %"
)
igpu_engines_video_wait = Gauge(
    "igpu_engines_video_wait", "Video wait utilisation %"
)

igpu_engines_video_enhance_busy = Gauge(
    "igpu_engines_video_enhance_busy", "Video Enhance busy utilisation %"
)
igpu_engines_video_enhance_sema = Gauge(
    "igpu_engines_video_enhance_sema", "Video Enhance sema utilisation %"
)
igpu_engines_video_enhance_wait = Gauge(
    "igpu_engines_video_enhance_wait", "Video Enhance wait utilisation %"
)

igpu_engines_compute_busy = Gauge(
    "igpu_engines_compute_busy", "Compute busy utilisation %"
)
igpu_engines_compute_sema = Gauge(
    "igpu_engines_compute_sema", "Compute sema utilisation %"
)
igpu_engines_compute_wait = Gauge(
    "igpu_engines_compute_wait", "Compute wait utilisation %"
)

igpu_client_engine_busy = Gauge(
    "igpu_client_engine_busy",
    "Per-client engine busy utilisation %",
    ["client_name", "pid", "engine"],
)
igpu_client_memory_system_total_bytes = Gauge(
    "igpu_client_memory_system_total_bytes",
    "Per-client system memory total",
    ["client_name", "pid"],
)
igpu_client_memory_system_resident_bytes = Gauge(
    "igpu_client_memory_system_resident_bytes",
    "Per-client system memory resident",
    ["client_name", "pid"],
)
igpu_client_memory_local_total_bytes = Gauge(
    "igpu_client_memory_local_total_bytes",
    "Per-client local memory total",
    ["client_name", "pid"],
)
igpu_client_memory_local_resident_bytes = Gauge(
    "igpu_client_memory_local_resident_bytes",
    "Per-client local memory resident",
    ["client_name", "pid"],
)

igpu_frequency_actual = Gauge("igpu_frequency_actual", "Frequency actual MHz")
igpu_frequency_requested = Gauge("igpu_frequency_requested", "Frequency requested MHz")

igpu_imc_bandwidth_reads = Gauge("igpu_imc_bandwidth_reads", "IMC reads MiB/s")
igpu_imc_bandwidth_writes = Gauge("igpu_imc_bandwidth_writes", "IMC writes MiB/s")

igpu_interrupts = Gauge("igpu_interrupts", "Interrupts/s")

igpu_period = Gauge("igpu_period", "Period ms")

igpu_power_gpu = Gauge("igpu_power_gpu", "GPU power W")
igpu_power_package = Gauge("igpu_power_package", "Package power W")

igpu_rc6 = Gauge("igpu_rc6", "RC6 %")

tracked_clients = {}


def update(data):
    global tracked_clients
    current_clients = {}

    # --- Global Metrics ---
    igpu_engines_blitter_busy.set(
        data.get("engines", {}).get("Blitter", {}).get("busy", 0.0)
    )
    igpu_engines_blitter_sema.set(
        data.get("engines", {}).get("Blitter", {}).get("sema", 0.0)
    )
    igpu_engines_blitter_wait.set(
        data.get("engines", {}).get("Blitter", {}).get("wait", 0.0)
    )
    igpu_engines_render_3d_busy.set(
        data.get("engines", {}).get("Render/3D", {}).get("busy", 0.0)
    )
    igpu_engines_render_3d_sema.set(
        data.get("engines", {}).get("Render/3D", {}).get("sema", 0.0)
    )
    igpu_engines_render_3d_wait.set(
        data.get("engines", {}).get("Render/3D", {}).get("wait", 0.0)
    )
    igpu_engines_video_busy.set(
        data.get("engines", {}).get("Video", {}).get("busy", 0.0)
    )
    igpu_engines_video_sema.set(
        data.get("engines", {}).get("Video", {}).get("sema", 0.0)
    )
    igpu_engines_video_wait.set(
        data.get("engines", {}).get("Video", {}).get("wait", 0.0)
    )
    igpu_engines_video_enhance_busy.set(
        data.get("engines", {}).get("VideoEnhance", {}).get("busy", 0.0)
    )
    igpu_engines_video_enhance_sema.set(
        data.get("engines", {}).get("VideoEnhance", {}).get("sema", 0.0)
    )
    igpu_engines_video_enhance_wait.set(
        data.get("engines", {}).get("VideoEnhance", {}).get("wait", 0.0)
    )
    igpu_engines_compute_busy.set(
        data.get("engines", {}).get("Compute", {}).get("busy", 0.0)
    )
    igpu_engines_compute_sema.set(
        data.get("engines", {}).get("Compute", {}).get("sema", 0.0)
    )
    igpu_engines_compute_wait.set(
        data.get("engines", {}).get("Compute", {}).get("wait", 0.0)
    )
    igpu_frequency_actual.set(data.get("frequency", {}).get("actual", 0))
    igpu_frequency_requested.set(data.get("frequency", {}).get("requested", 0))
    igpu_imc_bandwidth_reads.set(data.get("imc-bandwidth", {}).get("reads", 0))
    igpu_imc_bandwidth_writes.set(data.get("imc-bandwidth", {}).get("writes", 0))
    igpu_interrupts.set(data.get("interrupts", {}).get("count", 0))
    igpu_period.set(data.get("period", {}).get("duration", 0))
    igpu_power_gpu.set(data.get("power", {}).get("GPU", 0))
    igpu_power_package.set(data.get("power", {}).get("Package", 0))
    igpu_rc6.set(data.get("rc6", {}).get("value", 0))

    # --- Client Metrics ---
    clients_data = data.get("clients", {})
    for client_id, client_data in clients_data.items():
        client_name = client_data.get("name", "unknown")
        pid = client_data.get("pid", "unknown")
        client_key = (client_name, pid)

        # Update engine metrics
        engine_classes = client_data.get("engine-classes", {})
        current_clients[client_key] = {"engines": list(engine_classes.keys())}
        for engine_name, engine_data in engine_classes.items():
            busy_val = float(engine_data.get("busy", 0.0))
            igpu_client_engine_busy.labels(
                client_name=client_name, pid=pid, engine=engine_name
            ).set(busy_val)

        # Update memory metrics
        memory_data = client_data.get("memory", {})
        system_mem = memory_data.get("system", {})
        local_mem = memory_data.get("local", {})
        igpu_client_memory_system_total_bytes.labels(
            client_name=client_name, pid=pid
        ).set(float(system_mem.get("total", 0)))
        igpu_client_memory_system_resident_bytes.labels(
            client_name=client_name, pid=pid
        ).set(float(system_mem.get("resident", 0)))
        igpu_client_memory_local_total_bytes.labels(
            client_name=client_name, pid=pid
        ).set(float(local_mem.get("total", 0)))
        igpu_client_memory_local_resident_bytes.labels(
            client_name=client_name, pid=pid
        ).set(float(local_mem.get("resident", 0)))

    # Remove metrics for clients that are no longer running
    stale_client_keys = set(tracked_clients.keys()) - set(current_clients.keys())
    for client_key in stale_client_keys:
        client_name, pid = client_key

        # Remove engine metrics for the stale client
        if "engines" in tracked_clients[client_key]:
            for engine_name in tracked_clients[client_key]["engines"]:
                try:
                    igpu_client_engine_busy.remove(client_name, pid, engine_name)
                except KeyError:
                    pass  # Metric may not exist, safe to ignore

        # Remove memory metrics for the stale client
        try:
            igpu_client_memory_system_total_bytes.remove(client_name, pid)
            igpu_client_memory_system_resident_bytes.remove(client_name, pid)
            igpu_client_memory_local_total_bytes.remove(client_name, pid)
            igpu_client_memory_local_resident_bytes.remove(client_name, pid)
        except KeyError:
            pass  # Metric may not exist, safe to ignore

    # Update the global tracker
    tracked_clients = current_clients


if __name__ == "__main__":
    if os.getenv("DEBUG", "") == "true":
        debug = logging.DEBUG
    else:
        debug = logging.INFO
    logging.basicConfig(format="%(asctime)s - %(message)s", level=debug)

    start_http_server(8080)

    period = os.getenv("REFRESH_PERIOD_MS", 10000)
    device = os.getenv("DEVICE")

    if device is not None:
        cmd = "intel_gpu_top -J -s {} -d {}".format(int(period), device)
    else:
        cmd = "intel_gpu_top -J -s {}".format(int(period))

    process = subprocess.Popen(
        cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )

    logging.info("Started " + cmd)
    output = ""

    if os.getenv("IS_DOCKER", False):
        for line in process.stdout:
            line = line.decode("utf-8").strip()
            output += line

            try:
                data = json.loads(output.strip(","))
                logging.debug(data)
                update(data)
                output = ""
            except json.JSONDecodeError:
                continue
    else:
        while process.poll() is None:
            read = process.stdout.readline()
            output += read.decode("utf-8")
            logging.debug(output)
            if read == b"},\n":
                update(json.loads(output[:-2]))
                output = ""

    process.kill()

    if process.returncode != 0:
        logging.error("Error: " + process.stderr.read().decode("utf-8"))

    logging.info("Finished")
