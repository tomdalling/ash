require 'ash'
require 'pp'
require 'parslet/rig/rspec'

RSpec.describe Ash::Parser do
  it 'parses' do
    strs = [
      # I know
      'shi vene',
      # I don't know
      'shi navene',
      # I know you
      'shi vene shae',
      # I gave you mother nature's coffee
      # lit: I gave coffee of mother of world to you
      'shi vaebet shacafe ko sashir ko selt kun shae',
      # I love your manly mother
      # lit: I love mother manly of you
      'shi vamore sashir lashe ko shae',
      # Eat food
      'vese ses',
      # Will you eat food?
      # lit: ? you will-eat food
      'ka shae vesem ses',
      # I will know you before tomorrow
      'shi venem shae timet sha-tomorrow',
      # I drank your coffee because I wanted it
      # lit: I drank coffee of you because I wanted it
      'shi veket shacafe ko shae tozet shi volet shel',
    ]
    begin
      strs.each do |s|
        puts s
        result = Ash.parse(s)
        expect(result).not_to be_nil
        result
      end

      pp Ash.parse(strs.last)
    rescue Parslet::ParseFailed => error
      puts error.cause.ascii_tree
    end
  end

  def should_parse(rule, strs)
    parser = Ash::Parser.new.send(rule)
    strs.each do |s|
      expect(parser).to parse(s)
    end
  end

  it 'parses adjuncts' do
    should_parse(:temporal_adjunct, [
      'time sha-tomorrow', # at/on tomorrow
      'timet sha-tomorrow', # before tomorrow
      'timem sha-tomorrow', # after tomorrow
    ])
    should_parse(:instrumental_adjunct, [
      'tem shi', # with me
      'temna shi', # without me
    ])
    should_parse(:causal_adjunct, [
      'tozem shi volet shel', # because I wanted it
      'tozet shi vapem', # so that I will sleep
    ])
  end
end
