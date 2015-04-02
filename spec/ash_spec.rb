require 'ash'
require 'pp'

RSpec.describe Ash::Parser do
  it 'transforms the raw AST' do
    result = Ash::Parser.new.send(:transform_ast, {a: [" 1 "]})
    expect(result).to eq({a: ["1"]})
  end

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
    ]
    strs.each do |s|
      puts s
      result = Ash.parse(s)
      expect(result).not_to be_nil
      result
    end

    pp Ash.parse(strs.last)
  end
end
