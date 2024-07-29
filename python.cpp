#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include <speex_preprocess.h>

#define STRINGIFY(x) #x
#define MACRO_STRINGIFY(x) STRINGIFY(x)

#define SAMPLES_10_MS 160
#define BYTES_10_MS (SAMPLES_10_MS * 2)

namespace py = pybind11;

// ----------------------------------------------------------------------------

struct ProcessedAudioChunk {
  py::bytes audio;

  ProcessedAudioChunk() : audio("\0", BYTES_10_MS) {}
};

class AudioProcessor {
private:
  SpeexPreprocessState *state = NULL;

public:
  AudioProcessor(float auto_gain, int noise_suppression);
  ~AudioProcessor();

  std::unique_ptr<ProcessedAudioChunk> Process10ms(py::bytes audio);
};

AudioProcessor::AudioProcessor(float auto_gain, int noise_suppression) {
  this->state = speex_preprocess_state_init(SAMPLES_10_MS, 16000);

  int noise_state = (noise_suppression == 0) ? 0 : 1;
  speex_preprocess_ctl(state, SPEEX_PREPROCESS_SET_DENOISE, &noise_state);

  if (noise_suppression != 0) {
    speex_preprocess_ctl(state, SPEEX_PREPROCESS_SET_NOISE_SUPPRESS,
                         &noise_suppression);
  }

  int agc_enabled = (auto_gain > 0) ? 1 : 0;
  speex_preprocess_ctl(state, SPEEX_PREPROCESS_SET_AGC, &agc_enabled);
  if (auto_gain > 0) {
    speex_preprocess_ctl(state, SPEEX_PREPROCESS_SET_AGC_LEVEL, &auto_gain);
  }
}

std::unique_ptr<ProcessedAudioChunk>
AudioProcessor::Process10ms(py::bytes audio) {
  auto processed_chunk = std::make_unique<ProcessedAudioChunk>();

  py::buffer_info buffer_input(py::buffer(audio).request());
  py::buffer_info buffer_output(py::buffer(processed_chunk->audio).request());

  int16_t *ptr_input = static_cast<int16_t *>(buffer_input.ptr);
  int16_t *ptr_output = static_cast<int16_t *>(buffer_output.ptr);
  memcpy(ptr_output, ptr_input, BYTES_10_MS);
  speex_preprocess_run(this->state, ptr_output);

  return processed_chunk;
}

AudioProcessor::~AudioProcessor() {
  if (this->state) {
    speex_preprocess_state_destroy(this->state);
    this->state = NULL;
  }
}

// ----------------------------------------------------------------------------

PYBIND11_MODULE(speex_noise_cpp, m) {
  m.doc() = R"pbdoc(
        Noise suppression using speex
        -----------------------

        .. currentmodule:: speex_noise_cpp

        .. autosummary::
           :toctree: _generate

           AudioProcessor
    )pbdoc";

  py::class_<AudioProcessor>(m, "AudioProcessor")
      .def(py::init<float, int>())
      .def("Process10ms", &AudioProcessor::Process10ms);

  py::class_<ProcessedAudioChunk>(m, "ProcessedAudioChunk")
      .def_readonly("audio", &ProcessedAudioChunk::audio);

#ifdef VERSION_INFO
  m.attr("__version__") = MACRO_STRINGIFY(VERSION_INFO);
#else
  m.attr("__version__") = "dev";
#endif
}
