import Link from "next/link";
import { ArrowRight, Video, Zap, Shield, Sparkles } from "lucide-react";

export default function Home() {
  return (
    <div className="min-h-screen bg-black text-white selection:bg-purple-500/30 overflow-hidden relative">
      {/* Background gradients */}
      <div className="absolute top-0 -left-40 w-96 h-96 bg-purple-500 rounded-full mix-blend-multiply filter blur-[128px] opacity-50 animate-blob"></div>
      <div className="absolute top-0 -right-40 w-96 h-96 bg-blue-500 rounded-full mix-blend-multiply filter blur-[128px] opacity-50 animate-blob animation-delay-2000"></div>
      <div className="absolute -bottom-40 left-20 w-96 h-96 bg-pink-500 rounded-full mix-blend-multiply filter blur-[128px] opacity-50 animate-blob animation-delay-4000"></div>

      <main className="container mx-auto px-6 relative z-10">
        <nav className="flex items-center justify-between py-8">
          <div className="flex items-center gap-2">
            <Video className="w-8 h-8 text-purple-400" />
            <span className="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-purple-400 to-blue-400">
              MOV2MP4
            </span>
          </div>
          <div className="flex items-center gap-6">
            <Link href="/pricing" className="text-sm text-gray-300 hover:text-white transition-colors">Pricing</Link>
            <Link href="/login" className="text-sm text-gray-300 hover:text-white transition-colors">Login</Link>
          </div>
        </nav>

        <div className="flex flex-col items-center justify-center pt-32 pb-20 text-center max-w-4xl mx-auto">
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-white/5 border border-white/10 mb-8 backdrop-blur-sm">
            <Sparkles className="w-4 h-4 text-purple-400" />
            <span className="text-sm font-medium text-gray-300">Production-Ready Video Conversion</span>
          </div>
          
          <h1 className="text-5xl md:text-7xl font-extrabold tracking-tight mb-8">
            Convert MOV to MP4
            <br />
            <span className="bg-clip-text text-transparent bg-gradient-to-r from-purple-400 via-pink-400 to-blue-400">
              at Lightning Speed.
            </span>
          </h1>
          
          <p className="text-lg md:text-xl text-gray-400 mb-12 max-w-2xl leading-relaxed">
            Upload your massive MOV files and let our distributed cloud engine instantly convert them to MP4. No software required. Zero quality loss.
          </p>
          
          <Link href="/upload" className="group relative inline-flex items-center justify-center gap-3 px-8 py-4 bg-white text-black font-semibold rounded-full overflow-hidden transition-transform hover:scale-105 hover:shadow-[0_0_40px_rgba(255,255,255,0.3)]">
            <span className="relative z-10">Start Converting for Free</span>
            <ArrowRight className="w-5 h-5 relative z-10 group-hover:translate-x-1 transition-transform" />
            <div className="absolute inset-0 bg-gradient-to-r from-purple-200 to-blue-200 opacity-0 group-hover:opacity-100 transition-opacity"></div>
          </Link>
        </div>

        {/* Features Section */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 py-24 border-t border-white/10 mt-12">
          <div className="p-8 rounded-3xl bg-white/5 border border-white/10 backdrop-blur-sm">
            <div className="w-12 h-12 rounded-full bg-purple-500/20 flex items-center justify-center mb-6">
              <Zap className="w-6 h-6 text-purple-400" />
            </div>
            <h3 className="text-xl font-bold mb-4">Blazing Fast</h3>
            <p className="text-gray-400">Powered by a scalable network of Celery workers and optimized FFmpeg pipelines.</p>
          </div>
          <div className="p-8 rounded-3xl bg-white/5 border border-white/10 backdrop-blur-sm">
            <div className="w-12 h-12 rounded-full bg-blue-500/20 flex items-center justify-center mb-6">
              <Shield className="w-6 h-6 text-blue-400" />
            </div>
            <h3 className="text-xl font-bold mb-4">Secure & Private</h3>
            <p className="text-gray-400">Files are processed in memory or ephemeral storage and automatically deleted after conversion.</p>
          </div>
          <div className="p-8 rounded-3xl bg-white/5 border border-white/10 backdrop-blur-sm">
            <div className="w-12 h-12 rounded-full bg-pink-500/20 flex items-center justify-center mb-6">
              <Video className="w-6 h-6 text-pink-400" />
            </div>
            <h3 className="text-xl font-bold mb-4">Zero Quality Loss</h3>
            <p className="text-gray-400">Maintains original bitrate, frame rate, and resolution utilizing H.264 high-profile encoding.</p>
          </div>
        </div>
      </main>
    </div>
  );
}
