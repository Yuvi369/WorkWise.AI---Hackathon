import React, { useState, useEffect } from 'react';
import { Brain, Users, Shield, Clock, TrendingUp, CheckCircle, Zap, ArrowRight, Play, Star } from 'lucide-react';

const WorkWiseHomepage = () => {
  const [currentFeature, setCurrentFeature] = useState(0);
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    setIsVisible(true);
    const interval = setInterval(() => {
      setCurrentFeature((prev) => (prev + 1) % 4);
    }, 3000);
    return () => clearInterval(interval);
  }, []);

  const features = [
    {
      icon: <Brain className="w-8 h-8" />,
      title: "AI-Driven Matching",
      description: "Intelligent employee-task matching using advanced algorithms"
    },
    {
      icon: <Shield className="w-8 h-8" />,
      title: "Policy Validation",
      description: "HR policy check using RAG before every assignment"
    },
    {
      icon: <Clock className="w-8 h-8" />,
      title: "Real-time Availability",
      description: "Leave and availability sync via HRMS APIs"
    },
    {
      icon: <TrendingUp className="w-8 h-8" />,
      title: "Smart Insights",
      description: "Transparent, explainable recommendations with analytics"
    }
  ];

  const benefits = [
    "Prevents employee overloading",
    "Ensures policy compliance",
    "Reduces assignment time by 70%",
    "Improves team efficiency",
    "Provides workload balance",
    "Offers transparent decision-making"
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 text-white overflow-hidden">
      {/* Animated Background Elements */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute -top-40 -right-40 w-80 h-80 bg-purple-500 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-pulse"></div>
        <div className="absolute -bottom-40 -left-40 w-80 h-80 bg-teal-500 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-pulse delay-1000"></div>
        <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-96 h-96 bg-cyan-500 rounded-full mix-blend-multiply filter blur-xl opacity-10 animate-pulse delay-2000"></div>
      </div>
      {/* Top-right corner: GitHub and Login icons */}
      

      {/* Navigation */}
      <nav className="relative z-10 px-6 py-4 flex justify-between items-center backdrop-blur-sm bg-white/5 border-b border-white/10">
        <div className="flex items-center space-x-3">
          <div className="w-12 h-12 bg-gradient-to-r from-purple-500 to-teal-500 rounded-lg flex items-center justify-center mr-2">
            <Brain className="w-6 h-6 text-white" />
          </div>
          <div className="flex flex-col gap-1">
             <span className="text-2xl font-bold bg-gradient-to-r from-purple-400 to-teal-400 bg-clip-text text-transparent">
                WorkWise.AI
              </span>
              <p className="text-sm text-gray-300 hidden md:block">
                Think wise. Assign wise. WorkWise.AI.
              </p>
            
          </div>
         
        </div>
        <div className="hidden md:flex space-x-8">
          <a href="#features" className="hover:text-purple-300 transition-colors">Features</a>
          <a href="#benefits" className="hover:text-purple-300 transition-colors">Benefits</a>
          <a href="#demo" className="hover:text-purple-300 transition-colors">Demo</a>
        </div>
        <div className="flex items-center space-x-4">
          <button className="bg-gradient-to-r from-purple-500 to-teal-500 px-6 py-2 rounded-full hover:from-purple-600 hover:to-teal-600 transition-all duration-300 transform hover:scale-105">
            Get Started
          </button>
          {/* GitHub Link */}
          <a
            href="https://github.com/"
            target="_blank"
            rel="noopener noreferrer"
            className="bg-white/10 hover:bg-white/20 p-2 rounded-full transition-colors border border-white/10 flex items-center"
            title="View on GitHub"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              className="w-6 h-6 text-white"
              fill="currentColor"
              viewBox="0 0 24 24"
            >
              <path d="M12 .297c-6.63 0-12 5.373-12 12 0 5.303 3.438 9.8 8.205 11.387.6.113.82-.258.82-.577 0-.285-.01-1.04-.015-2.04-3.338.724-4.042-1.61-4.042-1.61-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.084-.729.084-.729 1.205.084 1.84 1.236 1.84 1.236 1.07 1.834 2.809 1.304 3.495.997.108-.775.418-1.305.762-1.605-2.665-.305-5.466-1.334-5.466-5.93 0-1.31.469-2.381 1.236-3.221-.124-.303-.535-1.523.117-3.176 0 0 1.008-.322 3.301 1.23a11.52 11.52 0 0 1 3.003-.404c1.018.005 2.045.138 3.003.404 2.291-1.553 3.297-1.23 3.297-1.23.653 1.653.242 2.873.119 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.803 5.624-5.475 5.921.43.372.823 1.102.823 2.222 0 1.606-.014 2.898-.014 3.293 0 .322.216.694.825.576C20.565 22.092 24 17.592 24 12.297c0-6.627-5.373-12-12-12"/>
            </svg>
          </a>
          {/* Login Link */}
          <a
            href="/login"
            className="bg-white/10 hover:bg-white/20 p-2 rounded-full transition-colors border border-white/10 flex items-center"
            title="Login"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              className="w-6 h-6 text-white"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
              strokeWidth={2}
            >
              <path strokeLinecap="round" strokeLinejoin="round" d="M15.75 9A3.75 3.75 0 1 1 8.25 9a3.75 3.75 0 0 1 7.5 0zM4.5 19.5a7.5 7.5 0 0 1 15 0v.75a.75.75 0 0 1-.75.75h-13.5a.75.75 0 0 1-.75-.75v-.75z" />
            </svg>
          </a>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="relative z-10 px-6 py-20 text-center">
        <div className={`max-w-6xl mx-auto transition-all duration-1000 ${isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-10'}`}>
          <div className="mb-8">
            <div className="inline-flex items-center bg-gradient-to-r from-purple-500/20 to-teal-500/20 backdrop-blur-sm border border-purple-500/30 rounded-full px-4 py-2 mb-6">
              <Zap className="w-4 h-4 mr-2 text-yellow-400" />
              <span className="text-sm font-medium">Intelligent Task Assignment System</span>
            </div>
            <h1 className="text-6xl md:text-7xl font-bold mb-6 leading-tight">
              <span className="bg-gradient-to-r from-white via-purple-200 to-teal-200 bg-clip-text text-transparent">
                Smart Work Deserves
              </span>
              <br />
              <span className="bg-gradient-to-r from-purple-400 to-teal-400 bg-clip-text text-transparent">
                Smart Assignment
              </span>
            </h1>
            <p className="text-xl md:text-2xl text-gray-300 mb-8 max-w-3xl mx-auto leading-relaxed">
              Empower your HR teams with AI-driven task allocation that considers skills, availability, 
              and policies to make every assignment count.
            </p>
          </div>

          <div className="flex flex-col sm:flex-row gap-4 justify-center items-center mb-12">
            <button className="group bg-gradient-to-r from-purple-500 to-teal-500 px-8 py-4 rounded-full text-lg font-semibold hover:from-purple-600 hover:to-teal-600 transition-all duration-300 transform hover:scale-105 hover:shadow-2xl flex items-center">
              Start Free Trial
              <ArrowRight className="w-5 h-5 ml-2 group-hover:translate-x-1 transition-transform" />
            </button>
            <button className="group bg-white/10 backdrop-blur-sm border border-white/20 px-8 py-4 rounded-full text-lg font-semibold hover:bg-white/20 transition-all duration-300 flex items-center">
              <Play className="w-5 h-5 mr-2" />
              Watch Demo
            </button>
          </div>

          {/* Stats */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8 max-w-4xl mx-auto">
            <div className="text-center">
              <div className="text-3xl font-bold text-purple-400 mb-2">70%</div>
              <div className="text-gray-400">Faster Assignment</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold text-teal-400 mb-2">100%</div>
              <div className="text-gray-400">Policy Compliance</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold text-purple-400 mb-2">50%</div>
              <div className="text-gray-400">Workload Balance</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold text-teal-400 mb-2">24/7</div>
              <div className="text-gray-400">Availability Sync</div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="relative z-10 px-6 py-20 bg-gradient-to-r from-purple-900/20 to-teal-900/20 backdrop-blur-sm">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-bold mb-6 bg-gradient-to-r from-purple-400 to-teal-400 bg-clip-text text-transparent">
              Intelligent Features
            </h2>
            <p className="text-xl text-gray-300 max-w-2xl mx-auto">
              Our multi-agent AI architecture ensures every assignment is smart, compliant, and efficient.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {features.map((feature, index) => (
              <div
                key={index}
                className={`group p-8 rounded-2xl backdrop-blur-sm border transition-all duration-500 hover:scale-105 hover:shadow-2xl ${
                  index === currentFeature
                    ? 'bg-gradient-to-br from-purple-500/20 to-teal-500/20 border-purple-500/50'
                    : 'bg-white/5 border-white/10 hover:bg-white/10'
                }`}
              >
                <div className={`w-16 h-16 rounded-2xl flex items-center justify-center mb-6 transition-all duration-300 ${
                  index === currentFeature
                    ? 'bg-gradient-to-r from-purple-500 to-teal-500 text-white'
                    : 'bg-white/10 text-gray-400 group-hover:bg-gradient-to-r group-hover:from-purple-500 group-hover:to-teal-500 group-hover:text-white'
                }`}>
                  {feature.icon}
                </div>
                <h3 className="text-xl font-semibold mb-3 text-white">{feature.title}</h3>
                <p className="text-gray-400 group-hover:text-gray-300 transition-colors">
                  {feature.description}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Benefits Section */}
      <section id="benefits" className="relative z-10 px-6 py-20">
        <div className="max-w-6xl mx-auto">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
            <div>
              <h2 className="text-4xl md:text-5xl font-bold mb-6 bg-gradient-to-r from-purple-400 to-teal-400 bg-clip-text text-transparent">
                Why Choose WorkWise.AI?
              </h2>
              <p className="text-xl text-gray-300 mb-8 leading-relaxed">
                Transform your task allocation process with intelligent automation that considers every factor 
                that matters for successful project delivery.
              </p>
              <div className="space-y-4">
                {benefits.map((benefit, index) => (
                  <div key={index} className="flex items-center space-x-3 group">
                    <div className="w-6 h-6 bg-gradient-to-r from-purple-500 to-teal-500 rounded-full flex items-center justify-center flex-shrink-0 group-hover:scale-110 transition-transform">
                      <CheckCircle className="w-4 h-4 text-white" />
                    </div>
                    <span className="text-gray-300 group-hover:text-white transition-colors">{benefit}</span>
                  </div>
                ))}
              </div>
            </div>
            <div className="relative">
              <div className="bg-gradient-to-br from-purple-500/20 to-teal-500/20 backdrop-blur-sm border border-purple-500/30 rounded-3xl p-8 hover:shadow-2xl transition-all duration-300">
                <div className="text-center mb-6">
                  <Users className="w-16 h-16 mx-auto mb-4 text-purple-400" />
                  <h3 className="text-2xl font-bold text-white mb-2">Manager Dashboard</h3>
                  <p className="text-gray-400">Complete control with intelligent insights</p>
                </div>
                <div className="space-y-4">
                  <div className="flex items-center justify-between p-3 bg-white/5 rounded-lg">
                    <span className="text-sm text-gray-400">Task Assignments</span>
                    <div className="flex items-center">
                      <div className="w-3 h-3 bg-green-500 rounded-full mr-2"></div>
                      <span className="text-sm font-medium">Active</span>
                    </div>
                  </div>
                  <div className="flex items-center justify-between p-3 bg-white/5 rounded-lg">
                    <span className="text-sm text-gray-400">Policy Compliance</span>
                    <div className="flex items-center">
                      <Star className="w-4 h-4 text-yellow-400 mr-1" />
                      <span className="text-sm font-medium">100%</span>
                    </div>
                  </div>
                  <div className="flex items-center justify-between p-3 bg-white/5 rounded-lg">
                    <span className="text-sm text-gray-400">Team Efficiency</span>
                    <div className="flex items-center">
                      <TrendingUp className="w-4 h-4 text-teal-400 mr-1" />
                      <span className="text-sm font-medium">+47%</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="relative z-10 px-6 py-20 bg-gradient-to-r from-purple-900/30 to-teal-900/30 backdrop-blur-sm">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-4xl md:text-5xl font-bold mb-6 bg-gradient-to-r from-white to-gray-300 bg-clip-text text-transparent">
            Ready to Transform Your Task Assignment?
          </h2>
          <p className="text-xl text-gray-300 mb-8 max-w-2xl mx-auto">
            WorkWise.AI to make smarter, faster, and more efficient task allocation decisions.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <button className="group bg-gradient-to-r from-purple-500 to-teal-500 px-8 py-4 rounded-full text-lg font-semibold hover:from-purple-600 hover:to-teal-600 transition-all duration-300 transform hover:scale-105 hover:shadow-2xl flex items-center justify-center">
              Start Your Free Trial
              <ArrowRight className="w-5 h-5 ml-2 group-hover:translate-x-1 transition-transform" />
            </button>
            <button className="bg-white/10 backdrop-blur-sm border border-white/20 px-8 py-4 rounded-full text-lg font-semibold hover:bg-white/20 transition-all duration-300">
              Schedule Demo
            </button>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="relative z-10 px-6 py-12 bg-black/20 backdrop-blur-sm border-t border-white/10">
        <div className="max-w-6xl mx-auto text-center">
          <div className="flex items-center justify-center space-x-3 mb-6">
            <div className="w-10 h-10 bg-gradient-to-r from-purple-500 to-teal-500 rounded-lg flex items-center justify-center">
              <Brain className="w-6 h-6 text-white" />
            </div>
            <span className="text-2xl font-bold bg-gradient-to-r from-purple-400 to-teal-400 bg-clip-text text-transparent">
              WorkWise.AI
            </span>
          </div>
          <p className="text-gray-400 mb-4">
            Empowering organizations to make intelligent, fair, and efficient task allocation decisions.
          </p>
          {/* <p className="text-sm text-gray-500">
            © 2025 WorkWise.AI. All rights reserved.
          </p> */}
        </div>
      </footer>
    </div>
  );
};

export default WorkWiseHomepage;